from aiogram.fsm.state import State, StatesGroup

class ConversionState(StatesGroup):
    waiting_for_operation = State()
    waiting_for_amount = State()