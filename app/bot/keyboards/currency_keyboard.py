from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


CURRENCY_FLAGS: dict[str, str] = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "PLN": "🇵🇱",
    "GBP": "🇬🇧",
}


def get_base_currency_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{CURRENCY_FLAGS['USD']} USD",
                callback_data="base:USD",
            ),
            InlineKeyboardButton(
                text=f"{CURRENCY_FLAGS['EUR']} EUR",
                callback_data="base:EUR",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{CURRENCY_FLAGS['PLN']} PLN",
                callback_data="base:PLN",
            ),
            InlineKeyboardButton(
                text=f"{CURRENCY_FLAGS['GBP']} GBP",
                callback_data="base:GBP",
            ),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_target_currency_keyboard(base_currency: str) -> InlineKeyboardMarkup:
    available_currencies = ["USD", "EUR", "PLN", "GBP"]

    buttons: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []

    for currency in available_currencies:
        if currency == base_currency:
            continue

        row.append(
            InlineKeyboardButton(
                text=f"{CURRENCY_FLAGS[currency]} {currency}",
                callback_data=f"target:{base_currency}:{currency}",
            )
        )

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)