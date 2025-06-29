"""Initialize the database by creating all tables."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Print environment variables for debugging
print("Environment variables:")
for key, value in os.environ.items():
    if "DATABASE" in key or "DB" in key:
        print(f"{key}: {value}")

# Load environment variables from .env file with override
load_dotenv(override=True)

# Print DATABASE_URL after loading .env
print(f"DATABASE_URL from .env: {os.getenv('DATABASE_URL')}")

# Import models to ensure they are registered with SQLAlchemy
from sheily_light_api.models import Base
from sheily_light_api.core.database import DB_URL
print(f"DB_URL from database.py: {DB_URL}")

def init_db():
    """Create all database tables."""
    print(f"Connecting to database at {DB_URL}")
    engine = create_engine(DB_URL)
    
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
