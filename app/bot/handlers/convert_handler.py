from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.services.currency_service import CurrencyService
from app.bot.states.conversion_state import ConversionState


router = Router()


CURRENCY_FLAGS = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "PLN": "🇵🇱",
    "GBP": "🇬🇧",
}


def get_currency_flag(currency: str) -> str:
    return CURRENCY_FLAGS.get(currency.upper(), "🏳️")


def format_decimal(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


@router.message(ConversionState.waiting_for_amount, F.text)
async def process_conversion_amount(
    message: Message,
    state: FSMContext,
    currency_service: CurrencyService,
) -> None:
    raw_amount = (message.text or "").strip().replace(",", ".")

    try:
        amount = Decimal(raw_amount)
    except InvalidOperation:
        await message.answer("Please enter a valid number, for example: 100 or 12.50.")
        return

    if amount <= 0:
        await message.answer("Amount must be greater than 0.")
        return

    data = await state.get_data()
    base_currency = data.get("base_currency")
    target_currency = data.get("target_currency")

    if not base_currency or not target_currency:
        await message.answer("Currency data not found. Please restart with /start.")
        await state.clear()
        return

    try:
        converted_amount = currency_service.convert_currency(
            amount=float(amount),
            from_currency=base_currency,
            to_currency=target_currency,
        )
    except Exception as error:
        await message.answer(f"Conversion failed: {error}")
        await state.clear()
        return

    if converted_amount is None:
        await message.answer("Conversion failed. Please try again later.")
        await state.clear()
        return

    base_flag = get_currency_flag(base_currency)
    target_flag = get_currency_flag(target_currency)

    response_text = (
        f"💱 Currency Conversion\n\n"
        f"{base_flag} {format_decimal(amount)} {base_currency} = "
        f"{target_flag} {Decimal(str(converted_amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)} {target_currency}"
    )

    await message.answer(response_text)
    await state.clear()