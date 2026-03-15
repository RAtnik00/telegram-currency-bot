from aiogram.types import Message

from app.services.currency_service import CurrencyService


class RateHandler:
    def __init__(self, currency_service: CurrencyService) -> None:
        self._currency_service = currency_service

    async def handle(self, message: Message) -> None:
        text = (message.text or "").strip()
        parts = text.split()

        if len(parts) < 2:
            await message.answer("Usage: /rate USD")
            return

        currency = parts[1].upper()

        try:
            rates = self._currency_service.get_currency_rate(currency)

            if not rates:
                await message.answer(f"Unable to retrieve rates for {currency}.")
                return

            eur = rates.get("EUR")
            gbp = rates.get("GBP")
            pln = rates.get("PLN")

            lines = [f"Exchange rate for {currency}:"]

            if eur is not None:
                lines.append(f"EUR: {eur}")
            if gbp is not None:
                lines.append(f"GBP: {gbp}")
            if pln is not None:
                lines.append(f"PLN: {pln}")

            await message.answer("\n".join(lines))

        except Exception as error:
            print(f"RateHandler error: {error}")
            await message.answer(f"Error retrieving exchange rate: {error}")