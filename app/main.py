import asyncio

from app.bot.bot_app import BotApplication
from app.bot.handlers.rate_handler import RateHandler
from app.bot.handlers.start_handler import StartHandler
from app.clients.currency_api_client import CurrencyApiClient
from app.config.settings import Settings
from app.services.currency_service import CurrencyService


async def main() -> None:
    settings = Settings.from_env()

    api_client = CurrencyApiClient()
    currency_service = CurrencyService(api_client)

    start_handler = StartHandler()
    rate_handler = RateHandler(currency_service)

    bot_app = BotApplication(
        settings=settings,
        start_handler=start_handler,
        rate_handler=rate_handler,
    )

    await bot_app.run()


if __name__ == "__main__":
    asyncio.run(main())