from pydantic import BaseModel, Field


class InspectChannelsRequest(BaseModel):
    limit: int = Field(gt=0, le=20, description="количество обрабатываемых каналов")
    batch_size: int = Field(gt=0, le=20)
