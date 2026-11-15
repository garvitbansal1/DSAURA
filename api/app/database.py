import os
import logging
import socket
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

db_url = settings.DATABASE_URL

# Check if running in Vercel / serverless environment
is_vercel = any(os.getenv(k) is not None for k in ["VERCEL", "VERCEL_ENV", "NOW_REGION", "LAMBDA_TASK_ROOT"])

def is_socket_reachable(host: str, port: int, timeout: float = 0.2) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

# In Vercel serverless environment without a remote DB configured, use SQLite in /tmp
if is_vercel and ("localhost" in db_url or "127.0.0.1" in db_url):
    db_url = "sqlite:////tmp/dsaura_v3.db"
elif "localhost" in db_url or "127.0.0.1" in db_url:
    # Fast check if local Postgres port 5432 is open before attempting psycopg2
    try:
        parsed = urlparse(db_url)
        host = parsed.hostname or "localhost"
        port = parsed.port or 5432
        if not is_socket_reachable(host, port, timeout=0.2):
            logger.info(f"PostgreSQL port {port} on {host} is unreachable. Falling back to SQLite.")
            db_url = "sqlite:///dsaura_fallback.db"
    except Exception:
        pass

# Normalize standard PostgreSQL prefixes for psycopg2
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

is_sqlite = db_url.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {"connect_timeout": 3}
engine_kwargs = {"pool_pre_ping": True}
if not is_sqlite:
    engine_kwargs.update({"pool_size": 5, "max_overflow": 10})

try:
    engine = create_engine(
        db_url,
        connect_args=connect_args,
        **engine_kwargs
    )
    if not is_sqlite:
        with engine.connect() as conn:
            pass
except Exception as e:
    logger.warning(f"Failed to connect to database {db_url}: {e}. Falling back to SQLite.")
    fallback_path = "/tmp/dsaura_v3.db" if is_vercel else "dsaura_fallback.db"
    db_url = f"sqlite:///{fallback_path}"
    engine = create_engine(db_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
