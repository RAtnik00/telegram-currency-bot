from aiogram.types import Message

from app.bot.keyboards.currency_keyboard import get_base_currency_keyboard


class StartHandler:
    async def handle(self, message: Message) -> None:
        await message.answer(
            "Welcome to Currency Bot!\n\n"
            "Available commands:\n"
            "/rate USD - get exchange rates\n"
            "/rate USD buy - get buy rates\n"
            "/rate USD sell - get sell rates\n\n"
            "Choose base currency:",
            reply_markup=get_base_currency_keyboard(page=0),
        )