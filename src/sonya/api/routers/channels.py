from fastapi import APIRouter, File, UploadFile

from sonya.services.upload import upload

router = APIRouter()


import re


def normalize_channel(link: str) -> str:
    """Приводит ссылку к единому виду для сравнения уникальности."""
    link = link.strip().lower()
    link = re.sub(r"^https?://", "", link)
    link = re.sub(r"^(t\.me|telegram\.me)/", "", link)
    link = re.sub(r"^@", "", link)
    link = link.rstrip("/")
    return link


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
