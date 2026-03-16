import asyncio
import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from app.bot.handlers.start_handler import StartHandler
from app.bot.handlers.rate_handler import RateHandler
from app.bot.handlers.callback_handler import CurrencyCallbackHandler
from app.bot.handlers.convert_handler import router as convert_router
from app.cache.currency_cache import CurrencyCache
from app.clients.currency_api_client import CurrencyApiClient
from app.services.currency_service import CurrencyService
from app.validators.currency_validator import CurrencyValidator


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


async def main() -> None:
    load_dotenv()

    setup_logging()

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")

    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    storage = MemoryStorage()

    api_client = CurrencyApiClient()
    cache = CurrencyCache(ttl_seconds=300)
    currency_validator = CurrencyValidator()
    currency_service = CurrencyService(
        api_client=api_client,
        cache=cache,
    )

    dp = Dispatcher(
        storage=storage,
        currency_service=currency_service,
    )

    start_handler = StartHandler()
    rate_handler = RateHandler(
        currency_service=currency_service,
        currency_validator=currency_validator,
    )
    callback_handler = CurrencyCallbackHandler()

    dp.message.register(start_handler.handle, Command("start"))
    dp.message.register(rate_handler.handle, Command("rate"))

    dp.callback_query.register(
        callback_handler.handle_base_currency,
        F.data.startswith("base:"),
    )
    dp.callback_query.register(
        callback_handler.handle_target_currency,
        F.data.startswith("target:"),
    )

    dp.include_router(convert_router)

    logging.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())