import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

db_url = settings.DATABASE_URL

# In Vercel serverless environment without a remote PostgreSQL DB configured, use SQLite in /tmp
is_vercel = os.getenv("VERCEL") is not None
if is_vercel and ("localhost" in db_url or "127.0.0.1" in db_url):
    db_url = "sqlite:////tmp/dsaura.db"

# Normalize standard PostgreSQL prefixes for psycopg2
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

is_sqlite = db_url.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}
engine_kwargs = {"pool_pre_ping": True}
if not is_sqlite:
    engine_kwargs.update({"pool_size": 10, "max_overflow": 20})

try:
    engine = create_engine(
        db_url,
        connect_args=connect_args,
        **engine_kwargs
    )
except Exception as e:
    logger.warning(f"Failed to initialize database {db_url}: {e}. Falling back to SQLite.")
    db_url = "sqlite:////tmp/dsaura.db"
    engine = create_engine("sqlite:////tmp/dsaura.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
