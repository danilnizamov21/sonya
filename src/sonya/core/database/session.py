import os
from contextlib import contextmanager
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(Path(__file__).resolve().parent / ".env")

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


@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
