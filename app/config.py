from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MOVIES_DB_URL: str
    BUCKET_NAME: str
    AWSAccessKeyId: str
    AWSSecretKey: str

    class Config:
        env_file = ".env"


settings = Settings()
