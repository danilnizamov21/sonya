from enum import StrEnum


class Status(StrEnum):
    PENDING = "pending"
    ACCESSIBLE = "accessible"
    PRIVATE = "private"
    TIMEOUT = "timeout"
    ERROR = "error"
