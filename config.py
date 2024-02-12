from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="PACKAGE_")
    db_url: str = "mysql+asyncmy://user:password@localhost:3306/db?charset=utf8mb4"
    db_echo: bool = False


settings = Settings()

REQUIRED_PACKAGES_TYPES_NAMES = ["одежда", "электроника", "разное"]


class ShippingCostState(Enum):
    present = "present"
    absent = "absent"
