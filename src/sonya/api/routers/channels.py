from fastapi import APIRouter, File, UploadFile

router = APIRouter()


@router.post("/upload")
def upload_channels(file: UploadFile = File(...)):
    text = file.file.read().decode("utf-8-sig")

    channels = [line.strip() for line in text.splitlines() if line.strip()]

    for channel in channels:
        print(channel)

    return {"status": "OK", "count": len(channels)}
