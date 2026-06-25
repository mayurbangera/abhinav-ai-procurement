def map_conversation_to_supplier(data: dict):

    is_msme_value = str(
        data.get("is_msme", "")
    ).upper()

    declaration_value = str(
        data.get("declaration_accepted", "")
    ).upper()

    return {

        "company_name":
            data.get("company_name"),

        "principal_business":
            data.get("principal_business"),

        "business_classification":
            "SUPPLIER",

        "gst_number":
            data.get("gst_number"),

        "pan_number":
            "NOT_PROVIDED",

        "date_of_incorporation":
            None,

        "registered_address":
            data.get("registered_address"),

        "godown_address":
            None,

        "contact_person_name":
            data.get("contact_person_name"),

        "contact_person_mobile":
            data.get("whatsapp_number"),

        "contact_person_email":
            data.get("contact_person_email"),

        "telephone_number":
            None,

        "whatsapp_number":
            data.get("whatsapp_number"),

        "supplier_category":
            data.get("supplier_category"),

        "material_types":
            data.get("material_types"),

        "bank_account_name":
            data.get("beneficiary_name"),

        "bank_account_number":
            data.get("bank_account_number"),

        "bank_ifsc":
            data.get("bank_ifsc"),

        "bank_name":
            data.get("bank_name"),

        "branch_name":
            data.get("branch_name"),

        "is_msme":
            is_msme_value == "YES",

        "msme_number":
            None if data.get("msme_number") == "SKIP"
            else data.get("msme_number"),

        "msme_certificate_path":
            None if data.get("msme_certificate_path") == "SKIP"
            else data.get("msme_certificate_path"),

        "gst_certificate_path":
            data.get("gst_certificate_path"),

        "customer_reference_1":
            data.get("references"),

        "customer_reference_2":
            None,

        "customer_reference_3":
            None,

        "customer_reference_4":
            None,

        "customer_reference_5":
            None,

        "authorized_person_name":
            data.get("authorized_person_name"),

        "designation":
            data.get("designation"),

        "declaration_accepted":
            declaration_value == "YES"
    }