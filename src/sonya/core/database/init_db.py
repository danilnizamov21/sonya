import logging

from sonya.core.logging import configure_logging

configure_logging()

from sonya.core.database.models import Base
from sonya.core.database.session import engine

logger = logging.getLogger(__name__)

try:
    Base.metadata.create_all(engine)
    logger.info("Database tables initialized")
except Exception:
    logger.exception("Database initialization failed")
    raise
