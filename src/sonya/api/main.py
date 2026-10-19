from fastapi import FastAPI

from sonya.api.routers.telegram import router as telegram
from sonya.api.routers.tgstat import router as tgstat

app = FastAPI()

app.include_router(telegram, prefix="/telegram", tags=["Telegram"])
app.include_router(tgstat, prefix="/tgstat", tags=["TGstat"])
