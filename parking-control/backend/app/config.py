from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    db_username: str
    db_password: str
    db_host: str
    db_name: str = "parking_control"

    # AWS
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str = "us-east-1"
    s3_bucket: str

    # Cognito
    cognito_user_pool_id: str
    cognito_client_id: str
    cognito_client_secret: str

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Camera
    camera_endpoint: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings() 