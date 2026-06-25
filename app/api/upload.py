from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

import os
import shutil
import uuid

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

GST_UPLOAD_FOLDER = "uploads/gst"
MSME_UPLOAD_FOLDER = "uploads/msme"

os.makedirs(
    GST_UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    MSME_UPLOAD_FOLDER,
    exist_ok=True
)


@router.post("/gst-certificate")
def upload_gst_certificate(
    file: UploadFile = File(...)
):

    allowed_extensions = [
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png"
    ]

    file_extension = os.path.splitext(
        file.filename
    )[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG, JPEG, PNG files allowed"
        )

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    max_size = 5 * 1024 * 1024

    if file_size > max_size:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB"
        )

    unique_filename = (
        str(uuid.uuid4()) + file_extension
    )

    file_path = os.path.join(
        GST_UPLOAD_FOLDER,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message": "GST Certificate Uploaded Successfully",
        "file_path": file_path,
        "file_size_bytes": file_size
    }


@router.post("/msme-certificate")
def upload_msme_certificate(
    file: UploadFile = File(...)
):

    allowed_extensions = [
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png"
    ]

    file_extension = os.path.splitext(
        file.filename
    )[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG, JPEG, PNG files allowed"
        )

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    max_size = 5 * 1024 * 1024

    if file_size > max_size:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB"
        )

    unique_filename = (
        str(uuid.uuid4()) + file_extension
    )

    file_path = os.path.join(
        MSME_UPLOAD_FOLDER,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message": "MSME Certificate Uploaded Successfully",
        "file_path": file_path,
        "file_size_bytes": file_size
    }