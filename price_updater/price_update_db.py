from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models import PackageDB
from price_updater.usd_price import get_usd_price
from api.utility.logging_config import logging


async def calculate_shipping_cost(package, usd_price):
    shipping_cost = (
        Decimal(package.weight) * Decimal("0.5")
        + package.package_cost * Decimal("0.01")
    ) * Decimal(usd_price)
    logging.info("Success calculate_shipping_cost: %s", shipping_cost)
    return shipping_cost


async def update_shipping_cost(session: AsyncSession):
    stmt = await session.execute(select(PackageDB))

    logging.info(
        "stmt in db for shipping_cost_update: %s",
        stmt,
    )
    packages = stmt.scalars().all()
    if packages:
        usd_price = await get_usd_price()
        logging.info("Packages in db for shipping_cost_update:")
        for package in packages:
            logging.info("%s", package)
            package_shipping_cost = await calculate_shipping_cost(package, usd_price)
            package.shipping_cost = package_shipping_cost
    try:
        await session.commit()
        logging.info("Success shipping_costs update in db")
    except SQLAlchemyError as se:
        logging.exception("SQLAlchemy error in shipping_cost update: %s", str(se))
        await session.rollback()
    finally:
        await session.close()
