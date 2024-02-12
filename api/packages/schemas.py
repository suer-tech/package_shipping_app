from pydantic import BaseModel, AfterValidator, Field
from decimal import Decimal
from typing import List, Optional, Annotated, Union

from config import REQUIRED_PACKAGES_TYPES_NAMES


class PackageType(BaseModel):
    id: int
    name: str


def validate_allowed_package_types(v: str) -> str:
    if v in REQUIRED_PACKAGES_TYPES_NAMES:
        return v
    raise ValueError(
        f"Got {v!r} package_type excepted one of {REQUIRED_PACKAGES_TYPES_NAMES}"
    )


AllowedPackagesTypeName = Annotated[str, AfterValidator(validate_allowed_package_types)]


class PackageBase(BaseModel):
    name: str
    weight: Decimal
    package_type: AllowedPackagesTypeName
    package_cost: Decimal


class PackageUpdate(PackageBase):
    shipping_cost: Optional[Union[str, Decimal]] | None = Field(None, exclude=False)

    def __init__(self, **data):
        super().__init__(**data)
        if self.shipping_cost is None:
            self.shipping_cost = "Не рассчитано"


class Package(PackageBase):
    pass


class PackageResponse(BaseModel):
    message: str
    id: int
