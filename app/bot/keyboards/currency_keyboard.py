from math import ceil

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


CURRENCY_FLAGS: dict[str, str] = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "PLN": "🇵🇱",
    "GBP": "🇬🇧",
    "CHF": "🇨🇭",
    "CZK": "🇨🇿",
    "UAH": "🇺🇦",
    "CAD": "🇨🇦",
    "AUD": "🇦🇺",
    "JPY": "🇯🇵",
}

AVAILABLE_CURRENCIES: list[str] = [
    "USD",
    "EUR",
    "PLN",
    "GBP",
    "CHF",
    "CZK",
    "UAH",
    "CAD",
    "AUD",
    "JPY",
]

CURRENCIES_PER_PAGE = 6
BUTTONS_PER_ROW = 2


def _paginate_currencies(
    currencies: list[str],
    page: int,
) -> tuple[list[str], int]:
    total_pages = max(1, ceil(len(currencies) / CURRENCIES_PER_PAGE))
    safe_page = max(0, min(page, total_pages - 1))

    start_index = safe_page * CURRENCIES_PER_PAGE
    end_index = start_index + CURRENCIES_PER_PAGE

    return currencies[start_index:end_index], total_pages


def _build_currency_buttons(
    currencies: list[str],
    callback_prefix: str,
) -> list[list[InlineKeyboardButton]]:
    buttons: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []

    for currency in currencies:
        row.append(
            InlineKeyboardButton(
                text=f"{CURRENCY_FLAGS.get(currency, '🏳️')} {currency}",
                callback_data=f"{callback_prefix}:{currency}",
            )
        )

        if len(row) == BUTTONS_PER_ROW:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    return buttons


def get_base_currency_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    page_currencies, total_pages = _paginate_currencies(AVAILABLE_CURRENCIES, page)

    buttons = _build_currency_buttons(
        currencies=page_currencies,
        callback_prefix="base",
    )

    navigation_row: list[InlineKeyboardButton] = []

    if page > 0:
        navigation_row.append(
            InlineKeyboardButton(
                text="⬅️ Prev",
                callback_data=f"page:base:{page - 1}",
            )
        )

    navigation_row.append(
        InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}",
            callback_data="noop",
        )
    )

    if page < total_pages - 1:
        navigation_row.append(
            InlineKeyboardButton(
                text="Next ➡️",
                callback_data=f"page:base:{page + 1}",
            )
        )

    buttons.append(navigation_row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_target_currency_keyboard(
    base_currency: str,
    page: int = 0,
) -> InlineKeyboardMarkup:
    filtered_currencies = [
        currency for currency in AVAILABLE_CURRENCIES if currency != base_currency
    ]
    page_currencies, total_pages = _paginate_currencies(filtered_currencies, page)

    buttons = _build_currency_buttons(
        currencies=page_currencies,
        callback_prefix=f"target:{base_currency}",
    )

    navigation_row: list[InlineKeyboardButton] = []

    if page > 0:
        navigation_row.append(
            InlineKeyboardButton(
                text="⬅️ Prev",
                callback_data=f"page:target:{base_currency}:{page - 1}",
            )
        )

    navigation_row.append(
        InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}",
            callback_data="noop",
        )
    )

    if page < total_pages - 1:
        navigation_row.append(
            InlineKeyboardButton(
                text="Next ➡️",
                callback_data=f"page:target:{base_currency}:{page + 1}",
            )
        )

    buttons.append(navigation_row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)