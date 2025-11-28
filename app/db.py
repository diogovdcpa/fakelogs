import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker


def _default_sqlite_url() -> str:
    base_dir = "/tmp" if os.getenv("VERCEL") else os.getcwd()
    return f"sqlite:///{os.path.join(base_dir, 'data.db')}"


def _normalize_sqlite_url(database_url: str) -> str:
    if not database_url.startswith("sqlite"):
        return database_url
    if database_url == "sqlite:///:memory:":
        return database_url

    db_path = database_url.replace("sqlite:///", "", 1).split("?", 1)[0]
    if db_path.startswith("/"):
        return database_url

    base_dir = "/tmp" if os.getenv("VERCEL") else os.getcwd()
    abs_path = os.path.join(base_dir, db_path)
    return f"sqlite:///{abs_path}"


def _ensure_sqlite_dir(database_url: str) -> None:
    if not database_url.startswith("sqlite"):
        return
    if database_url == "sqlite:///:memory:":
        return

    db_path = database_url.replace("sqlite:///", "", 1).split("?", 1)[0]
    directory = os.path.dirname(db_path)
    if directory:
        os.makedirs(directory, exist_ok=True)


DATABASE_URL = os.getenv("DATABASE_URL") or _default_sqlite_url()
DATABASE_URL = _normalize_sqlite_url(DATABASE_URL)

_ensure_sqlite_dir(DATABASE_URL)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)

SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
)
Base = declarative_base()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()


def remove_session(_: object = None) -> None:
    SessionLocal.remove()
