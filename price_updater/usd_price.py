from decimal import Decimal
import aiohttp

from api.utility.logging_config import logging


async def get_usd_price() -> Decimal:
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json(content_type=None)
            usd_price_exchange = data["Valute"]["USD"]["Value"]
            logging.info("Success get usd_price_exchange: %s", usd_price_exchange)
            return usd_price_exchange
