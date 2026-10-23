from pydantic import BaseModel, Field

from sonya.core.collectors.telegram.status import Status


class InspectChannelsRequest(BaseModel):
    limit: int | None
    batch_size: int = Field(gt=0, le=20)
    status: Status | None


class LoginTelegramRequest(BaseModel):
    password: str
