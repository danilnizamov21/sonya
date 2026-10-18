from fastapi import FastAPI

from sonya.api.routers.telegram import router as telegram

app = FastAPI()

app.include_router(telegram, prefix="/telegram", tags=["Telegram"])
