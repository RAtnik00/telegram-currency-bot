from aiogram.types import Message

from app.services.currency_service import CurrencyService


class ConvertHandler:
    def __init__(self, currency_service: CurrencyService) -> None:
        self._currency_service = currency_service

    async def handle(self, message: Message) -> None:
        text = (message.text or "").strip()
        parts = text.split()

        if len(parts) != 4:
            await message.answer("Usage: /convert 100 USD PLN")
            return

        try:
            amount = float(parts[1])
        except ValueError:
            await message.answer("Amount must be a number.")
            return

        if amount <= 0:
            await message.answer("Amount must be greater than zero.")
            return

        from_currency = parts[2].upper()
        to_currency = parts[3].upper()

        try:
            result = self._currency_service.convert_currency(
                amount=amount,
                from_currency=from_currency,
                to_currency=to_currency,
            )

            if result is None:
                await message.answer("Conversion failed.")
                return

            await message.answer(
                f"{amount:g} {from_currency} = {result:.2f} {to_currency}"
            )
        except Exception as error:
            await message.answer(f"Error converting currency: {error}")