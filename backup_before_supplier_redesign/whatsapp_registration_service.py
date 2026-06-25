from sqlalchemy.orm import Session



from app.models.supplier_conversation import (
    SupplierConversation
)

from app.whatsapp.registration_flow import (
    WELCOME_MESSAGE,
    QUESTION_MAP,
    REGISTRATION_STEPS
)

from app.services.validation_service import (
    validate_gst,
    validate_pan,
    validate_mobile,
    validate_email,
    validate_ifsc,
    validate_bank_account,
    validate_date
)

from app.models.supplier import Supplier

from app.models.supplier_reference import (
    SupplierReference
)

from app.services.supplier_mapper import (
    map_conversation_to_supplier
)


def process_whatsapp_message(
    phone_number: str,
    message_text: str,
    db: Session
):

    conversation = db.query(
        SupplierConversation
    ).filter(
        SupplierConversation.phone_number == phone_number,
        SupplierConversation.conversation_status == "IN_PROGRESS"
    ).first()

    incoming_message = (
        message_text.strip().upper()
    )

    if not conversation:

        if incoming_message in [
            "HI",
            "HELLO",
            "HII"
        ]:

            return {
                "reply": WELCOME_MESSAGE
            }

        if incoming_message == "START":

            conversation = SupplierConversation(
                phone_number=phone_number,
                current_step="company_name",
                collected_data={},
                conversation_status="IN_PROGRESS"
            )

            db.add(conversation)

            db.commit()

            db.refresh(conversation)

            return {
                "reply":
                    QUESTION_MAP["company_name"]
            }

        return {
            "reply":
                "Please send HI to start supplier registration."
        }

    current_step = conversation.current_step

    data = conversation.collected_data or {}

    data[current_step] = message_text

    current_index = REGISTRATION_STEPS.index(
        current_step
    )

    next_index = current_index + 1

    if next_index >= len(
        REGISTRATION_STEPS
    ):

        conversation.collected_data = data

        supplier_data = map_conversation_to_supplier(
            data
        )

        try:

            new_supplier = Supplier(
                **supplier_data
            )

            db.add(new_supplier)

            db.flush()

            conversation.conversation_status = (
                "COMPLETED"
            )

            db.commit()

            return {
                "reply":
                    f"Registration completed successfully. Supplier ID: {new_supplier.id}"
            }

        except Exception as e:

            db.rollback()

            return {
                "reply":
                    f"Registration failed: {str(e)}"
            }

    next_step = REGISTRATION_STEPS[
        next_index
    ]

    conversation.collected_data = data

    conversation.current_step = next_step

    db.commit()

    return {
        "reply":
            QUESTION_MAP[next_step]
    }