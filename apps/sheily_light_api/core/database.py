from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from contextlib import contextmanager
import os

DB_URL = os.getenv("DATABASE_URL", "sqlite:///sheily.db")

engine = create_engine(
    DB_URL, echo=False, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Create tables if not exist on import for MVP
if DB_URL.startswith("sqlite"):
    # Avoid circular import; models will import Base after this file is executed.
    from importlib import import_module

    # ensure models module loaded regardless of cwd
    try:
        import_module("sheily_light_api.models")  # noqa: F401
    except ModuleNotFoundError:
        pass
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db():
    """FastAPI dependency that yields a SQLAlchemy session and closes it once the request ends."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
