import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from app.bot.handlers.convert_handler import ConvertHandler
from app.bot.handlers.rate_handler import RateHandler
from app.bot.handlers.start_handler import StartHandler
from app.clients.currency_api_client import CurrencyApiClient
from app.config.settings import Settings
from app.services.currency_service import CurrencyService


async def main() -> None:
    settings = Settings.from_env()

    bot = Bot(token=settings.telegram_token)
    dp = Dispatcher()

    api_client = CurrencyApiClient()
    currency_service = CurrencyService(api_client)

    start_handler = StartHandler()
    rate_handler = RateHandler(currency_service)
    convert_handler = ConvertHandler(currency_service)

    dp.message.register(start_handler.handle, Command("start"))
    dp.message.register(start_handler.handle, Command("help"))
    dp.message.register(rate_handler.handle, Command("rate"))
    dp.message.register(convert_handler.handle, Command("convert"))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())