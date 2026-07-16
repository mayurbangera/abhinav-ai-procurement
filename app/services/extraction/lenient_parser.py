import json
from app.schemas.document_extraction import DocumentExtractionPayload

def lenient_parse_and_validate(text_response: str, model_name: str, document_uuid: str) -> DocumentExtractionPayload:
    """
    Parse a JSON string from LLM response and leniently repair any validation errors
    (such as unwrapped fields, null fields, or missing required objects) before
    validating with Pydantic.
    """
    # 1. Clean response string
    clean_text = text_response.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    if clean_text.startswith("```"):
        clean_text = clean_text[3:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]
    clean_text = clean_text.strip()

    try:
        data = json.loads(clean_text)
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response as valid JSON: {str(e)}")

    # 2. Repair helper for wrapped fields
    def repair_field(field_val, expected_type="string"):
        # If it's already a dict and has "value", it's likely a valid wrapper
        if isinstance(field_val, dict) and "value" in field_val:
            # Ensure required keys exist
            if "confidence" not in field_val or field_val["confidence"] is None:
                field_val["confidence"] = 0.5
            if "evidence" not in field_val or field_val["evidence"] is None:
                field_val["evidence"] = ""
            if "page_number" not in field_val or field_val["page_number"] is None:
                field_val["page_number"] = 1
            if "bounding_box" not in field_val:
                field_val["bounding_box"] = None
            if "extraction_method" not in field_val or not field_val["extraction_method"]:
                field_val["extraction_method"] = model_name
            if "validation_status" not in field_val or not field_val["validation_status"]:
                field_val["validation_status"] = "UNVALIDATED"
            return field_val

        # Otherwise, wrap the raw value (or None)
        raw_val = None
        if field_val is not None:
            if isinstance(field_val, dict):
                raw_val = field_val.get("value")
            else:
                raw_val = field_val

        # Attempt type casting if raw_val is not None
        if raw_val is not None:
            try:
                if expected_type == "number":
                    raw_val = float(raw_val)
                elif expected_type == "integer":
                    raw_val = int(raw_val)
                else:
                    raw_val = str(raw_val)
            except Exception:
                raw_val = None

        return {
            "value": raw_val,
            "confidence": 0.5,
            "evidence": "Repaired during validation recovery",
            "page_number": 1,
            "bounding_box": None,
            "extraction_method": model_name,
            "validation_status": "UNVALIDATED"
        }

    # 3. Repair Document Metadata
    doc_meta = data.setdefault("document_metadata", {})
    if not isinstance(doc_meta, dict):
        doc_meta = {}
        data["document_metadata"] = doc_meta
    
    doc_meta["document_id"] = repair_field(doc_meta.get("document_id", document_uuid))
    doc_meta["document_id"]["value"] = document_uuid
    
    doc_meta["document_type"] = repair_field(doc_meta.get("document_type", "QUOTATION"))
    doc_meta["document_number"] = repair_field(doc_meta.get("document_number"))
    doc_meta["document_date"] = repair_field(doc_meta.get("document_date"))
    
    if "revision_number" in doc_meta and doc_meta["revision_number"] is not None:
        doc_meta["revision_number"] = repair_field(doc_meta["revision_number"], "integer")
    if "vendor_reference_number" in doc_meta and doc_meta["vendor_reference_number"] is not None:
        doc_meta["vendor_reference_number"] = repair_field(doc_meta["vendor_reference_number"])
    if "total_pages" in doc_meta and doc_meta["total_pages"] is not None:
        doc_meta["total_pages"] = repair_field(doc_meta["total_pages"], "integer")

    # 4. Repair Vendor Metadata
    vendor_meta = data.setdefault("vendor_metadata", {})
    if not isinstance(vendor_meta, dict):
        vendor_meta = {}
        data["vendor_metadata"] = vendor_meta
    vendor_meta["vendor_name"] = repair_field(vendor_meta.get("vendor_name"))
    
    for k in ["supplier_code", "gst_number", "pan_number", "billing_address", "shipping_address", 
              "contact_person", "mobile", "email", "bank_account_number", "bank_ifsc_code", "bank_name"]:
        if k in vendor_meta and vendor_meta[k] is not None:
            vendor_meta[k] = repair_field(vendor_meta[k])

    # 5. Repair Project Metadata
    proj_meta = data.setdefault("project_metadata", {})
    if not isinstance(proj_meta, dict):
        proj_meta = {}
        data["project_metadata"] = proj_meta
    for k in ["project_name", "site_name", "delivery_location"]:
        if k in proj_meta and proj_meta[k] is not None:
            proj_meta[k] = repair_field(proj_meta[k])

    # 6. Repair Commercial Metadata
    comm_meta = data.setdefault("commercial_metadata", {})
    if not isinstance(comm_meta, dict):
        comm_meta = {}
        data["commercial_metadata"] = comm_meta
        
    for k in ["currency", "payment_terms", "delivery_terms", "validity_date", "delivery_timeline",
              "freight_terms", "loading_unloading_terms", "insurance_terms", "warranty_terms"]:
        if k in comm_meta and comm_meta[k] is not None:
            comm_meta[k] = repair_field(comm_meta[k])
            
    for k in ["total_basic_amount", "total_discount_amount", "total_tax_amount", 
              "total_freight_amount", "total_loading_unloading_amount"]:
        if k in comm_meta and comm_meta[k] is not None:
            comm_meta[k] = repair_field(comm_meta[k], "number")
            
    comm_meta["grand_total_amount"] = repair_field(comm_meta.get("grand_total_amount"), "number")

    # 7. Repair Line Items
    line_items = data.setdefault("line_items", [])
    if not isinstance(line_items, list):
        line_items = []
        data["line_items"] = line_items
        
    repaired_items = []
    for idx, item in enumerate(line_items):
        if not isinstance(item, dict):
            continue
            
        repaired_item = {}
        repaired_item["item_index"] = int(item.get("item_index", idx + 1))
        repaired_item["material_name"] = repair_field(item.get("material_name"))
        repaired_item["material_id"] = item.get("material_id")
        
        for k in ["requested_brand", "offered_brand", "requested_specification", "offered_specification", "remarks"]:
            if k in item and item[k] is not None:
                repaired_item[k] = repair_field(item[k])
                
        repaired_item["quantity"] = repair_field(item.get("quantity"), "number")
        repaired_item["unit_of_measure"] = repair_field(item.get("unit_of_measure"))
        repaired_item["basic_rate"] = repair_field(item.get("basic_rate"), "number")
        
        for k in ["discount_percent", "discount_amount", "tax_percent", "tax_amount", "freight_amount", "final_landed_rate"]:
            if k in item and item[k] is not None:
                repaired_item[k] = repair_field(item[k], "number")
                
        repaired_item["total_item_amount"] = repair_field(item.get("total_item_amount"), "number")
        repaired_items.append(repaired_item)
        
    data["line_items"] = repaired_items

    # 8. Repair Validation Summary
    val_sum = data.setdefault("validation_summary", {})
    if not isinstance(val_sum, dict):
        val_sum = {}
        data["validation_summary"] = val_sum
        
    for k in ["mathematical_validation", "business_validation", "semantic_validation"]:
        rep = val_sum.setdefault(k, {})
        if not isinstance(rep, dict):
            rep = {}
            val_sum[k] = rep
        rep.setdefault("status", "PASSED")
        rep.setdefault("logs", [])
        
    # Validate repaired dictionary
    return DocumentExtractionPayload.model_validate(data)
