class CurrencyValidator:
    SUPPORTED_CURRENCIES: set[str] = {
        "AUD",
        "BGN",
        "BRL",
        "CAD",
        "CHF",
        "CNY",
        "CZK",
        "DKK",
        "EUR",
        "GBP",
        "HKD",
        "HUF",
        "IDR",
        "ILS",
        "INR",
        "ISK",
        "JPY",
        "KRW",
        "MXN",
        "MYR",
        "NOK",
        "NZD",
        "PHP",
        "PLN",
        "RON",
        "SEK",
        "SGD",
        "THB",
        "TRY",
        "USD",
        "ZAR",
    }

    def is_valid_currency(self, currency: str) -> bool:
        if not currency:
            return False

        normalized = currency.strip().upper()

        if len(normalized) != 3:
            return False

        return normalized in self.SUPPORTED_CURRENCIES