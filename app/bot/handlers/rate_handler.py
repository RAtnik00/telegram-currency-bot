from aiogram.types import Message

class RateHandler:
    async def handle(self, message: Message) -> None:
        text = (message.text or "").strip()
        parts = text.split()

        if len(parts) < 2:
            await message.answer("Usage: /rate USD")
            return

        currency_code = parts[1].upper()

        await message.answer(
            f"Command accepted. I will show the exchange rate for the currency: {currency_code}"
        )