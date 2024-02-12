from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from api.packages.schemas import (
    Package,
    PackageUpdate,
)
from api.utility.logging_config import logging
from models import PackageDB, PackageTypeDB, db_helper
from config import REQUIRED_PACKAGES_TYPES_NAMES, ShippingCostState


async def register_package(
    user_session_id: str, package_in: Package, session: AsyncSession
):
    logging.info("Package_in: %s", package_in)

    try:
        new_package = PackageDB(
            name=package_in.name,
            weight=package_in.weight,
            package_type=package_in.package_type,
            package_cost=package_in.package_cost,
            user_session_id=user_session_id,
        )
    except ValueError as e:
        logging.exception("Data format in register_package is incorrect.")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

    session.add(new_package)
    try:
        await session.commit()
    except SQLAlchemyError as se:
        logging.exception("SQLAlchemy error in register_package: %s", str(se))

    else:
        logging.info("Success add new_package in db: %s", package_in)
        await session.refresh(new_package)
        return new_package


async def get_all_package_types(session: AsyncSession):
    try:
        query = await session.execute(select(PackageTypeDB))
    except SQLAlchemyError as se:
        logging.exception("SQLAlchemy error in get_all_package_types: %s", str(se))

    else:
        result = query.scalars().all()

        logging.info("Package_types in db: %s", result)

        return result


async def get_user_packages(
    session: AsyncSession,
    user_session_id: str,
    shipping_cost_filter: ShippingCostState | None = None,
    limit: int = 10,
    offset: int = 0,
):
    stmt = select(PackageDB).where(PackageDB.user_session_id == user_session_id)
    if shipping_cost_filter:
        sc_filter = PackageDB.shipping_cost.is_(None)
        if shipping_cost_filter is ShippingCostState.present:
            sc_filter = PackageDB.shipping_cost.is_not(None)

        stmt = stmt.where(sc_filter)
    stmt = stmt.order_by(PackageDB.id).offset(offset).limit(limit)
    try:
        query = await session.execute(stmt)
    except SQLAlchemyError as se:
        logging.exception("SQLAlchemy error in get_user_package: %s", str(se))
    else:
        packages = query.scalars().all()
        if not packages:
            logging.info("No packages found for user_session_id: %s", user_session_id)
            return JSONResponse({"error": "Packages not found"})
        for package in packages:
            if package.shipping_cost is None:
                package.shipping_cost = "Не рассчитано"
        logging.info("All packages for user_session_id in db: %s", packages)
        return packages


async def get_package_by_id(package_id_in: int, session: AsyncSession):
    try:
        stmt = await session.execute(
            select(PackageDB).where(PackageDB.id == package_id_in)
        )
    except SQLAlchemyError as se:
        logging.exception("SQLAlchemy error in get_package_by_id: %s", str(se))

    else:
        package_by_id = stmt.scalar()
        if not package_by_id:
            logging.info("No package found by package_by_id: %s", package_by_id)
            return JSONResponse({"error": "Package by id not found"})

        logging.info("Package by id in db: %s", package_by_id)

        shipping_cost = "Не рассчитано"
        if package_by_id.shipping_cost is not None:
            shipping_cost = package_by_id.shipping_cost

        package = PackageUpdate(
            name=package_by_id.name,
            weight=package_by_id.weight,
            package_type=package_by_id.package_type,
            package_cost=package_by_id.package_cost,
            shipping_cost=shipping_cost,
        )

        logging.info("Package by id for response: %s", package_by_id)
        if isinstance(package.shipping_cost, Decimal):
            return package.model_dump(exclude={"id"})
        else:
            return package.model_dump(exclude={"id", "shipping_cost"})


async def create_packages_types():
    async with db_helper.session_factory() as session:
        try:
            stmt = select(PackageTypeDB.name)
            pacakge_types_names = (await session.scalars(stmt)).all()
            existing_package_types = set(pacakge_types_names)

            to_create = []
            for name in REQUIRED_PACKAGES_TYPES_NAMES:
                if name not in existing_package_types:
                    to_create.append(PackageTypeDB(name=name))
            if to_create:
                session.add_all(to_create)
                await session.commit()
        except SQLAlchemyError as se:
            logging.exception("SQLAlchemy error in create_packages_types: %s", str(se))

        else:
            logging.info("Success add package_types in db: %s", to_create)
