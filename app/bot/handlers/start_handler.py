from aiogram.types import Message

class StartHandler:
    async def handle(self, message: Message) -> None:
        await message.answer(
            "Hello! I am a currency exchange rate bot.\n\n"
            "Available commands:\n"
            "/start - lunch\n"
            "/help - help\n"
            "/rate USD - show currency rate"
        )