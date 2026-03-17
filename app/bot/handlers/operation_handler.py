from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.states.conversion_state import ConversionState


router = Router()


@router.callback_query(F.data.startswith("operation:"))
async def handle_operation_selection(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    operation_type = callback.data.split(":")[1]

    await state.update_data(operation_type=operation_type)
    await state.set_state(ConversionState.waiting_for_amount)

    await callback.message.answer(
        "Enter the amount to convert, for example: 100"
    )
    await callback.answer()