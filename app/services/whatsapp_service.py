import requests

from app.config.settings import (
    META_ACCESS_TOKEN,
    META_PHONE_NUMBER_ID
)


def send_text_message(
    phone_number: str,
    message: str
):

    url = (
        f"https://graph.facebook.com/v23.0/"
        f"{META_PHONE_NUMBER_ID}/messages"
    )

    headers = {
        "Authorization":
            f"Bearer {META_ACCESS_TOKEN}",

        "Content-Type":
            "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",

        "to": phone_number,

        "type": "text",

        "text": {
            "body": message
        }
    }

    # DEBUG INFORMATION
    print("\n========== WHATSAPP SEND DEBUG ==========")
    print("URL:", url)
    print("PHONE NUMBER ID:", META_PHONE_NUMBER_ID)
    print("TOKEN PREFIX:", META_ACCESS_TOKEN[:20])
    print("TO:", phone_number)
    try:
        print("PAYLOAD:", payload)
    except UnicodeEncodeError:
        print("PAYLOAD:", str(payload).encode("ascii", "ignore").decode("ascii"))
    print("=========================================\n")

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print("STATUS:", response.status_code)
    try:
        print("RESPONSE:", response.text)
    except UnicodeEncodeError:
        print("RESPONSE:", response.text.encode("ascii", "ignore").decode("ascii"))

    return response.json()