from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_operation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🟢 Buy", callback_data="operation:buy"),
                InlineKeyboardButton(text="🔴 Sell", callback_data="operation:sell"),
            ]
        ]
    )