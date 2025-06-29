import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / 'apps' / 'sheily_light_api' / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Print environment variables
print("Environment variables:")
for key, value in os.environ.items():
    if "DATABASE" in key or "DB" in key:
        print(f"{key}: {value}")

# Test database URL
print(f"\nDATABASE_URL from environment: {os.getenv('DATABASE_URL')}")
