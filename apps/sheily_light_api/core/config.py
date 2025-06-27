from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    secret_key: str = Field("changeme", env="API_SECRET")
    access_token_expire_minutes: int = 60

settings = Settings()
