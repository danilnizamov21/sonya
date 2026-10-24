import logging
import os
from contextlib import contextmanager

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import URL, create_engine, event
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

PG_PWD = os.getenv("PG_PWD")
PG_NAME = os.getenv("PG_NAME")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_USER = os.getenv("PG_USER", "postgres")

if not PG_PWD or not PG_NAME:
    raise RuntimeError("PG_PWD and PG_NAME must be set")

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=PG_USER,
    password=PG_PWD,
    host=PG_HOST,
    port=PG_PORT,
    database=PG_NAME,
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@event.listens_for(engine, "connect")
def _log_database_connection(*args: object) -> None:
    del args
    logger.info("Database connection established")


@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        logger.exception("Database transaction failed")
        db.rollback()
        raise
    finally:
        db.close()
