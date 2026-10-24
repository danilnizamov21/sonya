import logging
import re
import traceback
from logging.handlers import RotatingFileHandler
from pathlib import Path

_REDACTIONS = (
    (
        re.compile(
            r"(?i)\b(password|passwd|pwd|token|access_token|refresh_token|"
            r"api[_-]?key|secret)\b\s*[:=]\s*(?:\"[^\"]*\"|'[^']*'|[^\s,;]+)"
        ),
        r"\1=[REDACTED]",
    ),
    (
        re.compile(r"(?i)\bauthorization\s*[:=]\s*(?:bearer\s+)?[^\s,;]+"),
        "Authorization: [REDACTED]",
    ),
    (
        re.compile(r"(?i)(https?://)[^/@\s]+:[^/@\s]+@"),
        r"\1[REDACTED]@",
    ),
    (
        re.compile(r"(?i)\bhttps?://[^\s\"']+"),
        "[REDACTED_URL]",
    ),
    (
        re.compile(
            r"(?i)([?&](?:password|token|access_token|refresh_token|api[_-]?key)=)"
            r"[^&#\s]+"
        ),
        r"\1[REDACTED]",
    ),
    (
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "[REDACTED_EMAIL]",
    ),
    (
        re.compile(r"(?<!\w)\+?\d(?:[\s().-]*\d){9,14}(?!\w)"),
        "[REDACTED_PHONE]",
    ),
)


class _RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if (
            record.levelno >= logging.ERROR
            and not record.exc_info
            and not record.stack_info
        ):
            record = logging.makeLogRecord(record.__dict__.copy())
            stack = traceback.extract_stack()
            logging_path = Path(logging.__file__).resolve().parent
            stack = [
                frame
                for frame in stack[:-1]
                if Path(frame.filename).resolve().parent != logging_path
                and Path(frame.filename).resolve() != Path(__file__).resolve()
            ]
            record.stack_info = "Stack (most recent call last):\n" + "".join(
                traceback.format_list(stack)
            )

        message = super().format(record)
        for pattern, replacement in _REDACTIONS:
            message = pattern.sub(replacement, message)
        return message


def configure_logging() -> None:
    root_logger = logging.getLogger()
    if any(
        getattr(handler, "_sonya_logging_handler", False)
        for handler in root_logger.handlers
    ):
        return

    log_dir = Path.cwd() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    formatter = _RedactingFormatter(
        "%(asctime)s.%(msecs)03d %(levelname)s [%(name)s] "
        "%(filename)s:%(funcName)s:%(lineno)d %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    error_handler = RotatingFileHandler(
        log_dir / "error.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    for handler in (console_handler, error_handler):
        handler._sonya_logging_handler = True  # type: ignore[attr-defined]
        root_logger.addHandler(handler)

    root_logger.setLevel(logging.INFO)
    logging.getLogger("sonya").setLevel(logging.DEBUG)
    logging.getLogger("uvicorn.access").disabled = True