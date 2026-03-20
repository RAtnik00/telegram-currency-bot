from aiogram.types import Message

from app.services.currency_service import CurrencyService
from app.validators.currency_validator import CurrencyValidator


class RateHandler:
    def __init__(
        self,
        currency_service: CurrencyService,
        currency_validator: CurrencyValidator,
    ) -> None:
        self._currency_service = currency_service
        self._currency_validator = currency_validator

    async def handle(self, message: Message) -> None:
        text = (message.text or "").strip()
        parts = text.split()

        if len(parts) < 2:
            await message.answer("Usage: /rate USD or /rate USD buy or /rate USD sell")
            return

        currency = parts[1].upper()
        selected_rate_type = "general"

        if len(parts) >= 3:
            selected_rate_type = parts[2].lower()

        if selected_rate_type not in {"general", "buy", "sell"}:
            await message.answer(
                "Invalid rate type. Use: general, buy, or sell.\n"
                "Example: /rate USD sell"
            )
            return

        if not self._currency_validator.is_valid_currency(currency):
            await message.answer(
                "Unsupported currency. Please use a valid ISO code like USD, EUR, or PLN."
            )
            return

        try:
            rates = self._currency_service.get_currency_rate(currency)

            if not rates:
                await message.answer(f"Unable to retrieve exchange rates for {currency}.")
                return

            lines = [f"Exchange rates for {currency} ({selected_rate_type}):"]

            for target_currency, rate_values in rates.items():
                selected_rate = rate_values.get(selected_rate_type)

                if selected_rate is None:
                    continue

                lines.append(f"{target_currency}: {selected_rate:.4f}")

            if len(lines) == 1:
                await message.answer(
                    f"No {selected_rate_type} rates available for {currency}."
                )
                return

            await message.answer("\n".join(lines))

        except Exception as error:
            await message.answer(f"Error retrieving exchange rates: {error}")