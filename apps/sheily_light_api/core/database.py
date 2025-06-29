from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from contextlib import contextmanager
import os

# Debug: Print environment variables
print("Environment variables:")
for key, value in os.environ.items():
    if "DATABASE" in key or "DB" in key:
        print(f"{key}: {value}")

DB_URL = os.getenv("DATABASE_URL", "sqlite:///sheily.db")
print(f"Using database URL: {DB_URL}")

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


def get_db():
    """Dependency for FastAPI to get a database session."""
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()

# Alias para compatibilidad con código existente
get_db_dep = get_db
