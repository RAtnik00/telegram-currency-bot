from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from app.bot.handlers.rate_handler import RateHandler
from app.bot.handlers.start_handler import StartHandler
from app.config.settings import Settings


class BotApplication:
    def __init__(
        self,
        settings: Settings,
        start_handler: StartHandler,
        rate_handler: RateHandler,
    ) -> None:
        self._settings = settings
        self._start_handler = start_handler
        self._rate_handler = rate_handler

        self._bot = Bot(token=self._settings.telegram_token)
        self._dispatcher = Dispatcher()

    def setup_routes(self) -> None:
        self._dispatcher.message.register(self._start_handler.handle, Command("start"))
        self._dispatcher.message.register(self._start_handler.handle, Command("help"))
        self._dispatcher.message.register(self._rate_handler.handle, Command("rate"))

    async def run(self) -> None:
        self.setup_routes()
        await self._dispatcher.start_polling(self._bot)