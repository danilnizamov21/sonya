from fastapi import APIRouter, File, UploadFile

from sonya.core.services.upload import upload

router = APIRouter()


@router.post("/upload")
def upload_channels(file: UploadFile = File(...)):
    text = file.file.read().decode("utf-8-sig")

    raw_channels = [line.strip() for line in text.splitlines() if line.strip()]

    channels, duplicates = upload(raw_channels)
    return {
        "status": "OK",
        "count": len(channels),
        "duplicates_removed": len(duplicates),
        "duplicates": duplicates,
    }
