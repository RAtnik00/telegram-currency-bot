import asyncio

from app.bot.bot_app import BotApplication
from app.bot.handlers.rate_handler import RateHandler
from app.bot.handlers.start_handler import StartHandler
from app.config.settings import Settings


async def main() -> None:
    settings = Settings.from_env()

    start_handler = StartHandler()
    rate_handler = RateHandler()

    bot_app = BotApplication(
        settings=settings,
        start_handler=start_handler,
        rate_handler=rate_handler,
    )

    await bot_app.run()


if __name__ == "__main__":
    asyncio.run(main())