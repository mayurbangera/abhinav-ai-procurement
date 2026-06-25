import requests
import os
import uuid

from app.config.settings import (
    META_ACCESS_TOKEN
)


def get_media_url(media_id: str):

    url = (
        f"https://graph.facebook.com/v23.0/"
        f"{media_id}"
    )

    headers = {
        "Authorization":
            f"Bearer {META_ACCESS_TOKEN}"
    }

    response = requests.get(
        url,
        headers=headers
    )

    response.raise_for_status()

    return response.json()["url"]


def download_media(
    media_id: str,
    upload_folder: str
):

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    media_url = get_media_url(
        media_id
    )

    headers = {
        "Authorization":
            f"Bearer {META_ACCESS_TOKEN}"
    }

    response = requests.get(
        media_url,
        headers=headers
    )

    response.raise_for_status()

    filename = (
        str(uuid.uuid4()) + ".bin"
    )

    file_path = os.path.join(
        upload_folder,
        filename
    )

    with open(
        file_path,
        "wb"
    ) as file:

        file.write(
            response.content
        )

    return file_path