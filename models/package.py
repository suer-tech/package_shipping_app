from decimal import Decimal
from typing import Optional

from sqlalchemy import String, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PackageTypeDB(Base):

    name: Mapped[str] = mapped_column(String(100), unique=True)


class PackageDB(Base):

    name: Mapped[str] = mapped_column(String(100))
    weight: Mapped[Decimal] = mapped_column(DECIMAL(10, 2, asdecimal=True))
    package_type: Mapped[str] = mapped_column(ForeignKey(PackageTypeDB.name))
    package_cost: Mapped[Decimal] = mapped_column(DECIMAL(10, 2, asdecimal=True))
    shipping_cost: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(10, 2, asdecimal=True)
    )
    user_session_id: Mapped[str] = mapped_column(String(100))

    def __str__(self):
        return f"PackageDB(name={self.name}, weight={self.weight})"
