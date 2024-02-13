import asyncio

from celery import Celery

from config import settings
from models import db_helper
from price_updater.price_update_db import update_shipping_cost
from api.utility.logging_config import logging


celery = Celery(
    "celery_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery.conf.beat_schedule = {
    "run_periodic_task": {
        "task": "price_updater.celery_worker.periodic_start_update_shipping_cost",
        "schedule": 300,
    },
}


@celery.task
def periodic_start_update_shipping_cost():
    logging.info("periodic_start_update_shipping_cost")

    asyncio.run(update())

    logging.info("Success starting shipping cost update loop")


async def update():
    async with db_helper.session_factory() as session:
        logging.info("async with db_helper.session_factory() as session")
        await asyncio.create_task(update_shipping_cost(session=session))
