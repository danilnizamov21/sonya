from typing import Literal

from pydantic import BaseModel, Field

# Категории которые доступны с сайта тгстат
TopicType = Literal[
    "babies",
    "nature",
    "construction",
    "telegram",
    "instagram",
    "sales",
    "transport",
    "religion",
    "esoterics",
    "darknet",
    "gambling",
    "shock",
    "erotica",
    "adult",
    "other",
    "blogs",
    "news",
    "entertainment",
    "tech",
    "economics",
    "business",
    "crypto",
    "travels",
    "marketing",
    "psychology",
    "design",
    "politics",
    "art",
    "law",
    "education",
    "books",
    "language",
    "career",
    "edutainment",
    "courses",
    "sport",
    "beauty",
    "medicine",
    "health",
    "pics",
    "apps",
    "video",
    "music",
    "games",
    "food",
    "quotes",
    "handmade",
]


class TopicRequest(BaseModel):
    topic: TopicType
    pages: int = Field(default=5, gt=0, le=100)
