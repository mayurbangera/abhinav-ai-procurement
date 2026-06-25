WELCOME_MESSAGE = """
🏢 Welcome to Abhinav Group Supplier Registration

Thank you for your interest in becoming an approved supplier.

You will be required to answer 22 questions.

⚠️ Please answer every question carefully.

Skipping mandatory information or providing incorrect information may result in rejection of your supplier registration request.

During registration you will be asked to provide:

• Company Information
• GST Details
• Contact Information
• Supplier Category
• Material Types
• Banking Details
• MSME Information (Optional)
• Customer References
• GST Registration Certificate

To begin registration, please reply:

START
"""


REGISTRATION_STEPS = [

    "company_name",

    "principal_business",

    "gst_number",

    "registered_address",

    "contact_person_name",

    "contact_person_email",

    "whatsapp_number",

    "supplier_category",

    "material_types",

    "bank_name",

    "beneficiary_name",

    "bank_account_number",

    "bank_ifsc",

    "branch_name",

    "is_msme",

    "msme_number",

    "msme_certificate_path",

    "gst_certificate_path",

    "references",

    "authorized_person_name",

    "designation",

    "declaration_accepted"
]


QUESTION_MAP = {

    "company_name":
        "1️⃣ What is your Company Name?",

    "principal_business":
        "2️⃣ What work does your company do?\n\nExample:\nCement Supply\nSteel Supply\nElectrical Work",

    "gst_number":
        "3️⃣ Please enter your GST Number",

    "registered_address":
        "4️⃣ Please enter your Company Address",

    "contact_person_name":
        "5️⃣ Please enter Contact Person Name",

    "contact_person_email":
        "6️⃣ Please enter Email Address\n\n(Type SKIP if not available)",

    "whatsapp_number":
        "7️⃣ Please enter WhatsApp Number",

    "supplier_category":
        """8️⃣ Select Supplier Category

1 - Cement
2 - Steel
3 - Electrical
4 - Plumbing
5 - Hardware
6 - Paint
7 - Tiles
8 - Civil Contractor
9 - Labour Contractor
10 - Other""",

    "material_types":
        """9️⃣ What materials do you supply?

Example:

Cement

Steel

Cement, Steel, Sand

Type your answer.""",

    "bank_name":
        "🔟 Please enter Bank Name",

    "beneficiary_name":
        "1️⃣1️⃣ Please enter Account Holder Name",

    "bank_account_number":
        "1️⃣2️⃣ Please enter Bank Account Number",

    "bank_ifsc":
        "1️⃣3️⃣ Please enter IFSC Code",

    "branch_name":
        "1️⃣4️⃣ Please enter Bank Branch Name",

    "is_msme":
        "1️⃣5️⃣ Are you MSME Registered?\n\nReply YES or NO",

    "msme_number":
        "1️⃣6️⃣ Please enter MSME Number\n\nOr type SKIP",

    "msme_certificate_path":
        """1️⃣7️⃣ Please upload MSME Certificate

(PDF/JPG/PNG)

Or type SKIP""",

    "gst_certificate_path":
        """1️⃣8️⃣ Please upload GST Registration Certificate

(PDF/JPG/PNG)

This document is mandatory.""",

    "references":
        """1️⃣9️⃣ Please provide minimum 1 customer reference and maximum 3.

Format:

Company Name | Contact Person | Mobile Number

Example:

ABC Builders | Rajesh Sharma | 9876543210""",

    "authorized_person_name":
        "2️⃣0️⃣ Please enter your Name",

    "designation":
        "2️⃣1️⃣ Please enter your Designation",

    "declaration_accepted":
        """2️⃣2️⃣ Declaration

I confirm that all information provided is correct and true.

Reply YES to submit registration."""
}