from app.clients.currency_api_client import CurrencyApiClient


class CurrencyService:
    def __init__(self, api_client: CurrencyApiClient) -> None:
        self._api_client = api_client

    def get_currency_rate(self, currency: str) -> dict[str, float] | None:
        return self._api_client.get_latest_rates(
            base=currency,
            symbols=["EUR", "GBP", "PLN"],
        )

    def convert_currency(
        self,
        amount: float,
        from_currency: str,
        to_currency: str,
    ) -> float | None:
        if amount <= 0:
            return None

        if from_currency.upper() == to_currency.upper():
            return amount

        rates = self._api_client.get_latest_rates(
            base=from_currency,
            symbols=[to_currency],
        )

        if not rates:
            return None

        rate = rates.get(to_currency.upper())
        if rate is None:
            return None

        return amount * rate