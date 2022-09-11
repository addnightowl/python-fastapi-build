from pydantic import BaseSettings

"""Data validation and settings management using Python type annotations.
pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.
Define how data should be in pure, canonical Python; validate it with pydantic."""

"""
# example environment variable validation
class Settings(BaseSettings):
    database_password: str = "localhost"
    database_username: str = "postgres"
    secret_key: str = "12345678910"
# create an instance of the Settings() class
settings = Settings()
# access the setting properties


print(settings.database_password)
print(settings.database_username)
print(settings.secret_key)
"""

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:
        env_file = ".env" 

settings = Settings()

