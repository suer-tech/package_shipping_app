from dotenv import load_dotenv
import os
from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="PACKAGE_")
    redis_password: str = os.getenv("REDIS_PASSWORD")
    redis_port: str = os.getenv("REDIS_PORT")
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL")
    celery_result_backend: str = os.getenv("CELERY_RESULT_BACKEND")
    package_db_url: str = os.getenv("PACKAGE_DB_URL")
    db_root_password: str = os.getenv("MARIADB_ROOT_PASSWORD")
    db_user: str = os.getenv("MARIADB_USER")
    db_password: str = os.getenv("MARIADB_PASSWORD")
    db_name: str = os.getenv("MARIADB_DATABASE")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")
    db_url: str = (
        f"mysql+asyncmy://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
    )
    db_echo: bool = False


settings = Settings()


REQUIRED_PACKAGES_TYPES_NAMES = ["одежда", "электроника", "разное"]


class ShippingCostState(Enum):
    present = "present"
    absent = "absent"
