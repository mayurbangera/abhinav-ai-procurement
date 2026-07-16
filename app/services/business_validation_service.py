import os
import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.document_extraction import DocumentExtractionPayload, ValidationLogEntry
from app.services.document_intelligence_service import INGEST_FOLDER, get_ingested_document
from dateutil.parser import parse as parse_date

def validate_document_business(db: Session, document_uuid: str) -> dict:
    """
    Perform mathematical and business validations on the extracted quotation data.
    Updates the validation report logs inside the staging JSON file on disk.
    """
    log = get_ingested_document(db, document_uuid)
    if not log:
        raise HTTPException(
            status_code=404,
            detail=f"Ingestion log for document UUID '{document_uuid}' not found."
        )

    json_filename = f"{document_uuid}_extracted.json"
    json_path = os.path.join(INGEST_FOLDER, json_filename).replace("\\", "/")

    if not os.path.exists(json_path):
        raise HTTPException(
            status_code=400,
            detail=f"Structured JSON extraction output does not exist for UUID '{document_uuid}'."
        )

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            raw_json = f.read()
        payload = DocumentExtractionPayload.model_validate_json(raw_json)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read/parse existing extraction JSON file: {str(e)}"
        )

    # Helper to clean duplicate logs
    def clear_duplicate_logs(report, prefix):
        def get_rule_name(l):
            if isinstance(l, dict):
                return l.get("rule_name")
            return getattr(l, "rule_name", None)
        report.logs = [l for l in report.logs if not get_rule_name(l).startswith(prefix)]

    # ──────────────────────────────────────────────────────────
    # 1. Mathematical Validation
    # ──────────────────────────────────────────────────────────
    math_report = payload.validation_summary.mathematical_validation
    math_report.status = "PASSED"
    clear_duplicate_logs(math_report, "math_")

    total_calculated_items = 0.0
    math_failures = 0

    for item in payload.line_items:
        qty = item.quantity.value if item.quantity else None
        rate = item.basic_rate.value if item.basic_rate else None
        extracted_total = item.total_item_amount.value if item.total_item_amount else None
        
        if qty is None or rate is None:
            continue

        # Expected basic amount
        expected_basic = qty * rate
        
        # Apply discount
        discount_val = 0.0
        if item.discount_percent and item.discount_percent.value is not None:
            discount_val = expected_basic * (item.discount_percent.value / 100.0)
        elif item.discount_amount and item.discount_amount.value is not None:
            discount_val = item.discount_amount.value
            
        taxable = expected_basic - discount_val
        
        # Apply tax
        tax_val = 0.0
        if item.tax_percent and item.tax_percent.value is not None:
            tax_val = taxable * (item.tax_percent.value / 100.0)
        elif item.tax_amount and item.tax_amount.value is not None:
            tax_val = item.tax_amount.value

        expected_total = taxable + tax_val
        
        # Add to grand total accumulator
        if extracted_total is not None:
            total_calculated_items += extracted_total
        else:
            total_calculated_items += expected_total

        # Validate with a threshold of 1.0 INR
        if extracted_total is not None and abs(expected_total - extracted_total) > 1.0:
            math_failures += 1
            math_report.status = "FAILED"
            math_report.logs.append(ValidationLogEntry(
                rule_name=f"math_item_{item.item_index}_total",
                status="FAILED",
                message=f"Item {item.item_index} ('{item.material_name.value if item.material_name else ''}'): "
                        f"Calculated amount {expected_total:.2f} differs from extracted amount {extracted_total:.2f}."
            ))
        else:
            math_report.logs.append(ValidationLogEntry(
                rule_name=f"math_item_{item.item_index}_total",
                status="PASSED",
                message=f"Item {item.item_index} total check passed (Calculated: {expected_total:.2f})."
            ))

    # Validate Grand Total
    extracted_grand = payload.commercial_metadata.grand_total_amount.value if payload.commercial_metadata.grand_total_amount else None
    if extracted_grand is not None:
        # Check if grand total matches sum of item totals (standard for landed totals)
        diff = abs(total_calculated_items - extracted_grand)
        if diff > 2.0:
            math_failures += 1
            math_report.status = "FAILED"
            math_report.logs.append(ValidationLogEntry(
                rule_name="math_grand_total",
                status="FAILED",
                message=f"Quotation grand total mismatch: Sum of items total is {total_calculated_items:.2f}, "
                        f"but extracted grand total is {extracted_grand:.2f} (diff: {diff:.2f})."
            ))
        else:
            math_report.logs.append(ValidationLogEntry(
                rule_name="math_grand_total",
                status="PASSED",
                message=f"Grand total matches sum of items (Calculated: {total_calculated_items:.2f})."
            ))

    # ──────────────────────────────────────────────────────────
    # 2. Business Validation
    # ──────────────────────────────────────────────────────────
    biz_report = payload.validation_summary.business_validation
    biz_report.status = "PASSED"
    clear_duplicate_logs(biz_report, "biz_")

    # A. Check Validity / Expiry age
    doc_date_field = payload.document_metadata.document_date
    doc_date_val = doc_date_field.value if doc_date_field else None
    
    if doc_date_val:
        try:
            parsed_date = parse_date(str(doc_date_val))
            # Make timezone aware if needed
            if parsed_date.tzinfo is None:
                parsed_date = parsed_date.replace(tzinfo=timezone.utc)
            
            current_time = datetime.now(timezone.utc)
            age_days = (current_time - parsed_date).days
            
            # If quote is older than 30 days, raise a warning
            if age_days > 30:
                if biz_report.status != "FAILED":
                    biz_report.status = "WARNING"
                biz_report.logs.append(ValidationLogEntry(
                    rule_name="biz_quotation_expiry",
                    status="WARNING",
                    message=f"Quotation was dated {doc_date_val} ({age_days} days ago). It exceeds the standard 30-day validity period."
                ))
            else:
                biz_report.logs.append(ValidationLogEntry(
                    rule_name="biz_quotation_expiry",
                    status="PASSED",
                    message=f"Quotation is fresh (Dated {doc_date_val}, {age_days} days ago)."
                ))
        except Exception as e:
            # Date parse warning
            if biz_report.status != "FAILED":
                biz_report.status = "WARNING"
            biz_report.logs.append(ValidationLogEntry(
                rule_name="biz_quotation_expiry",
                status="WARNING",
                message=f"Could not parse document date '{doc_date_val}' for age verification: {str(e)}"
            ))
    else:
        if biz_report.status != "FAILED":
            biz_report.status = "WARNING"
        biz_report.logs.append(ValidationLogEntry(
            rule_name="biz_quotation_expiry",
            status="WARNING",
            message="Quotation date is missing. Cannot verify validity period."
        ))

    # B. Check payment and delivery terms
    pay_terms = payload.commercial_metadata.payment_terms.value if payload.commercial_metadata.payment_terms else None
    del_terms = payload.commercial_metadata.delivery_terms.value if payload.commercial_metadata.delivery_terms else None

    if not pay_terms:
        if biz_report.status != "FAILED":
            biz_report.status = "WARNING"
        biz_report.logs.append(ValidationLogEntry(
            rule_name="biz_payment_terms",
            status="WARNING",
            message="Payment terms are missing from the quotation. Please clarify before drafting PO."
        ))
    else:
        biz_report.logs.append(ValidationLogEntry(
            rule_name="biz_payment_terms",
            status="PASSED",
            message="Payment terms present."
        ))

    if not del_terms:
        if biz_report.status != "FAILED":
            biz_report.status = "WARNING"
        biz_report.logs.append(ValidationLogEntry(
            rule_name="biz_delivery_terms",
            status="WARNING",
            message="Delivery terms are missing from the quotation."
        ))
    else:
        biz_report.logs.append(ValidationLogEntry(
            rule_name="biz_delivery_terms",
            status="PASSED",
            message="Delivery/Freight terms present."
        ))

    # Overwrite JSON file back to disk
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(payload.model_dump_json(indent=2))
    except OSError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save validated JSON file back to disk: {str(e)}"
        )

    return payload.model_dump()
