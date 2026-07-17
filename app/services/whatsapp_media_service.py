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
        f"https://graph.facebook.com/v19.0/"
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


from fastapi import HTTPException

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

    # Fetch using stream=True to check content length first
    response = requests.get(
        media_url,
        headers=headers,
        stream=True
    )

    response.raise_for_status()

    # Verify content length does not exceed 10 MB
    content_length = response.headers.get("Content-Length")
    if content_length:
        size_bytes = int(content_length)
        if size_bytes > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"Uploaded file size ({round(size_bytes / (1024 * 1024), 2)} MB) exceeds 10 MB limit."
            )

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

    # Write in chunks of 8KB to avoid buffering large files entirely in memory
    bytes_downloaded = 0
    with open(
        file_path,
        "wb"
    ) as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                bytes_downloaded += len(chunk)
                if bytes_downloaded > 10 * 1024 * 1024:
                    file.close()
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    raise HTTPException(
                        status_code=400,
                        detail="File download exceeded maximum allowed size of 10 MB."
                    )
                file.write(chunk)

    # Convert Windows path separators to URL separators
    return file_path.replace("\\", "/")