from aiogram.types import Message

from app.bot.keyboards.currency_keyboard import get_base_currency_keyboard


class StartHandler:
    async def handle(self, message: Message) -> None:
        await message.answer(
            "Welcome to Currency Bot!\n\n"
            "Available commands:\n"
            "/rate USD - get exchange rates\n"
            "/convert 100 USD PLN - convert currency\n\n"
            "Or use the button below to start currency selection:",
            reply_markup=get_base_currency_keyboard(page=0),
        )