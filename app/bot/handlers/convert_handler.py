from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot.states.conversion_state import ConversionState
from app.services.currency_service import CurrencyService


class ConvertHandler:
    def __init__(self, currency_service: CurrencyService) -> None:
        self._currency_service = currency_service

    async def process_conversion_amount(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        raw_amount = (message.text or "").strip().replace(",", ".")

        try:
            amount = Decimal(raw_amount)
        except InvalidOperation:
            await message.answer("Please enter a valid amount.")
            return

        if amount <= 0:
            await message.answer("Amount must be greater than zero.")
            return

        data = await state.get_data()
        base_currency = data.get("base_currency")
        target_currency = data.get("target_currency")
        operation_type = data.get("operation_type", "general")

        if not base_currency or not target_currency:
            await message.answer("Currency data is missing. Please start again.")
            await state.clear()
            return

        converted_amount = self._currency_service.convert_currency(
            amount=amount,
            from_currency=base_currency,
            to_currency=target_currency,
            rate_type=operation_type,
        )

        if converted_amount is None:
            await message.answer("Failed to convert currency. Please try again later.")
            return

        converted_amount = converted_amount.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        await message.answer(
            f"{amount} {base_currency} = {converted_amount} {target_currency}\n"
            f"Rate type: {operation_type}"
        )

        await state.clear()