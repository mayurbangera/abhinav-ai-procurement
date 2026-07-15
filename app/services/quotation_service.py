from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from app.models.quotation import Quotation
from app.models.quotation_item import QuotationItem

class QuotationService:

    @staticmethod
    def _generate_quotation_number(db: Session) -> str:
        year = datetime.now().year
        next_val = db.execute(text("SELECT nextval('quotation_number_seq')")).scalar()
        return f"QT-{year}-{next_val:04d}"

    @staticmethod
    def create_quotation(db: Session, data: dict) -> Quotation:
        # Check if there is an existing quotation for this RFQ + Vendor
        existing_quotes = db.query(Quotation).filter(
            Quotation.rfq_id == data["rfq_id"],
            Quotation.vendor_id == data["vendor_id"]
        ).order_by(Quotation.revision_number.desc()).all()

        if existing_quotes:
            # We are creating a revision
            latest_existing = existing_quotes[0]
            base_quotation_number = latest_existing.quotation_number
            new_revision_number = latest_existing.revision_number + 1
            
            # Deprecate older quotes
            for eq in existing_quotes:
                eq.is_latest = False
        else:
            # First quotation
            base_quotation_number = QuotationService._generate_quotation_number(db)
            new_revision_number = 0

        # Create Header
        quotation = Quotation(
            quotation_number=base_quotation_number,
            revision_number=new_revision_number,
            rfq_id=data["rfq_id"],
            vendor_id=data["vendor_id"],
            is_latest=True,
            date_received=data["date_received"],
            validity_date=data.get("validity_date"),
            payment_terms=data.get("payment_terms"),
            delivery_timeline=data.get("delivery_timeline"),
            freight_amount_total=data.get("freight_amount_total", 0.0),
            loading_unloading_total=data.get("loading_unloading_total", 0.0),
            attachment_path=data.get("attachment_path"),
            status="Submitted",
            creation_source=data.get("creation_source", "MANUAL"),
            created_by=data["created_by"]
        )
        
        db.add(quotation)
        db.flush() # Get quotation.id

        grand_total = float(quotation.freight_amount_total) + float(quotation.loading_unloading_total)

        # Create Items and calculate math
        for item_data in data["items"]:
            if not item_data.get("is_quoted", True):
                # Item not quoted
                qi = QuotationItem(
                    quotation_id=quotation.id,
                    rfq_item_id=item_data["rfq_item_id"],
                    is_quoted=False
                )
                db.add(qi)
                continue

            basic_rate = float(item_data.get("basic_rate", 0.0))
            discount_pct = float(item_data.get("discount_percent", 0.0))
            tax_pct = float(item_data.get("tax_percent", 0.0))
            freight = float(item_data.get("freight_amount", 0.0))
            qty = float(item_data.get("quoted_quantity", 0.0))

            # Math Logic
            discount_amount = basic_rate * (discount_pct / 100.0)
            taxable_amount = basic_rate - discount_amount
            tax_amount = taxable_amount * (tax_pct / 100.0)
            
            final_landed_rate = taxable_amount + tax_amount + freight
            total_item_amount = final_landed_rate * qty

            grand_total += total_item_amount

            qi = QuotationItem(
                quotation_id=quotation.id,
                rfq_item_id=item_data["rfq_item_id"],
                is_quoted=True,
                quoted_quantity=qty,
                brand_offered=item_data.get("brand_offered"),
                specs_offered=item_data.get("specs_offered", {}),
                basic_rate=basic_rate,
                discount_percent=discount_pct,
                tax_percent=tax_pct,
                freight_amount=freight,
                final_landed_rate=final_landed_rate,
                total_item_amount=total_item_amount,
                remarks=item_data.get("remarks")
            )
            db.add(qi)

        # Update header grand total
        quotation.grand_total = grand_total

        db.commit()
        db.refresh(quotation)
        return quotation

    @staticmethod
    def get_quotation(db: Session, quotation_id: int) -> Quotation:
        return db.query(Quotation).filter(Quotation.id == quotation_id).first()

    @staticmethod
    def get_rfq_quotations(db: Session, rfq_id: int, only_latest: bool = True) -> list:
        query = db.query(Quotation).filter(Quotation.rfq_id == rfq_id)
        if only_latest:
            query = query.filter(Quotation.is_latest == True)
        return query.order_by(Quotation.vendor_id, Quotation.revision_number.desc()).all()
