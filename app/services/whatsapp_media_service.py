import os
import uuid
import requests

from app.config.settings import (
    META_ACCESS_TOKEN
)


def get_media_url(
    media_id: str
):

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

    content_type = response.headers.get(
        "Content-Type",
        ""
    ).lower()

    extension_map = {
        "application/pdf": ".pdf",
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png"
    }

    file_extension = extension_map.get(
        content_type,
        ".bin"
    )

    filename = (
        str(uuid.uuid4())
        + file_extension
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

    # Convert Windows path separators to URL separators
    return file_path.replace("\\", "/")