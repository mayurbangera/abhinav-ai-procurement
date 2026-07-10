from datetime import datetime
from sqlalchemy.orm import Session

from app.models.rfq import RFQ
from app.models.rfq_item import RFQItem
from app.models.rfq_vendor import RFQVendor
from app.models.supplier import Supplier


class RFQService:

    @staticmethod
    def _generate_rfq_number(db: Session) -> str:
        """Generate sequential RFQ number: RFQ-2026-001."""
        year = datetime.now().year
        last = (
            db.query(RFQ)
            .order_by(RFQ.id.desc())
            .first()
        )
        if last and last.rfq_number:
            try:
                seq = int(last.rfq_number.split("-")[-1]) + 1
            except (ValueError, IndexError):
                seq = 1
        else:
            seq = 1
        return f"RFQ-{year}-{seq:03d}"

    # ──────────────────────────────────────────────────
    # RFQ CRUD
    # ──────────────────────────────────────────────────

    @staticmethod
    def create_rfq(db: Session, data: dict) -> RFQ:
        rfq = RFQ(
            rfq_number=RFQService._generate_rfq_number(db),
            project_name=data["project_name"],
            site_name=data["site_name"],
            delivery_location=data["delivery_location"],
            payment_terms=data.get("payment_terms"),
            created_by=data["created_by"],
            status="Draft"
        )
        db.add(rfq)
        db.commit()
        db.refresh(rfq)
        return rfq

    @staticmethod
    def get_rfq(db: Session, rfq_id: int) -> RFQ:
        return db.query(RFQ).filter(RFQ.id == rfq_id).first()

    @staticmethod
    def list_rfqs(db: Session, status: str = None) -> list:
        query = db.query(RFQ)
        if status:
            query = query.filter(RFQ.status == status)
        return query.order_by(RFQ.created_at.desc()).all()

    @staticmethod
    def update_status(db: Session, rfq_id: int, status: str) -> RFQ:
        rfq = db.query(RFQ).filter(RFQ.id == rfq_id).first()
        if rfq:
            rfq.status = status
            db.commit()
            db.refresh(rfq)
        return rfq

    # ──────────────────────────────────────────────────
    # RFQ Items
    # ──────────────────────────────────────────────────

    @staticmethod
    def add_item(db: Session, rfq_id: int, data: dict) -> RFQItem:
        item = RFQItem(
            rfq_id=rfq_id,
            material_category=data["material_category"],
            material_name=data["material_name"],
            quantity=data["quantity"],
            unit=data["unit"],
            brand_required=data.get("brand_required"),
            dynamic_fields=data.get("dynamic_fields") or {},
            remarks=data.get("remarks")
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def get_items(db: Session, rfq_id: int) -> list:
        return db.query(RFQItem).filter(RFQItem.rfq_id == rfq_id).all()

    # ──────────────────────────────────────────────────
    # RFQ Vendors
    # ──────────────────────────────────────────────────

    @staticmethod
    def add_vendor(db: Session, rfq_id: int, vendor_id: int) -> RFQVendor:
        existing = (
            db.query(RFQVendor)
            .filter(
                RFQVendor.rfq_id == rfq_id,
                RFQVendor.vendor_id == vendor_id
            )
            .first()
        )
        if existing:
            return existing

        rv = RFQVendor(
            rfq_id=rfq_id,
            vendor_id=vendor_id
        )
        db.add(rv)
        db.commit()
        db.refresh(rv)
        return rv

    @staticmethod
    def get_vendors(db: Session, rfq_id: int) -> list:
        return (
            db.query(RFQVendor)
            .filter(RFQVendor.rfq_id == rfq_id)
            .all()
        )

    # ──────────────────────────────────────────────────
    # Send via WhatsApp
    # ──────────────────────────────────────────────────

    @staticmethod
    def send_rfq_to_vendors(
        db: Session,
        rfq_id: int,
        deadline: str = None,
        contact_person: str = None,
        contact_number: str = None
    ) -> dict:
        from app.services.rfq_whatsapp_service import generate_rfq_whatsapp_message
        from app.services.whatsapp_service import send_text_message

        rfq = db.query(RFQ).filter(RFQ.id == rfq_id).first()
        if not rfq:
            return {"error": "RFQ not found"}

        items = db.query(RFQItem).filter(RFQItem.rfq_id == rfq_id).all()
        rfq_vendors = (
            db.query(RFQVendor)
            .filter(RFQVendor.rfq_id == rfq_id)
            .all()
        )

        if not rfq_vendors:
            return {"error": "No vendors attached to this RFQ"}

        # Build item dicts
        item_dicts = [
            {
                "material_name": it.material_name,
                "material_category": it.material_category,
                "quantity": float(it.quantity),
                "unit": it.unit,
                "brand_required": it.brand_required,
                "dynamic_fields": it.dynamic_fields or {},
                "remarks": it.remarks
            }
            for it in items
        ]

        # Generate message once — same for all vendors
        message = generate_rfq_whatsapp_message(
            rfq_number=rfq.rfq_number,
            project_name=rfq.project_name,
            site_name=rfq.site_name,
            delivery_location=rfq.delivery_location,
            payment_terms=rfq.payment_terms,
            items=item_dicts,
            deadline=deadline,
            contact_person=contact_person,
            contact_number=contact_number
        )

        results = []
        for rv in rfq_vendors:
            vendor = db.query(Supplier).filter(Supplier.id == rv.vendor_id).first()
            if not vendor:
                continue

            phone = vendor.whatsapp_number
            # Normalize to international format
            if not phone.startswith("+"):
                phone = f"91{phone}" if len(phone) == 10 else phone

            wa_result = send_text_message(phone, message)

            rv.sent_at = datetime.now()
            rv.whatsapp_status = "Sent"
            db.commit()

            results.append({
                "vendor": vendor.company_name,
                "phone": phone,
                "result": wa_result
            })

        # Update RFQ status
        rfq.status = "Sent"
        db.commit()

        return {
            "rfq_number": rfq.rfq_number,
            "message_preview": message,
            "sent_to": results
        }
