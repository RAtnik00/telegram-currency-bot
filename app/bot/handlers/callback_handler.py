from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.keyboards.currency_keyboard import get_target_currency_keyboard
from app.bot.keyboards.operation_keyboard import get_operation_keyboard
from app.bot.states.conversion_state import ConversionState


class CurrencyCallbackHandler:
    async def handle_base_currency(self, callback: CallbackQuery) -> None:
        if callback.data is None or callback.message is None:
            await callback.answer()
            return

        _, base_currency = callback.data.split(":")

        await callback.message.answer(
            f"Base currency selected: {base_currency}\n\n"
            "Now choose the target currency:",
            reply_markup=get_target_currency_keyboard(base_currency),
        )
        await callback.answer()

    async def handle_target_currency(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        if callback.data is None or callback.message is None:
            await callback.answer()
            return

        _, base_currency, target_currency = callback.data.split(":")

        await state.update_data(
            base_currency=base_currency,
            target_currency=target_currency,
        )
        await state.set_state(ConversionState.waiting_for_operation)

        await callback.message.answer(
            f"Selected pair: {base_currency} → {target_currency}\n\n"
            "Choose the operation type:",
            reply_markup=get_operation_keyboard(),
        )
        await callback.answer()