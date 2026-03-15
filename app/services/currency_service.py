from app.clients.currency_api_client import CurrencyApiClient


class CurrencyService:
    def __init__(self, api_client: CurrencyApiClient) -> None:
        self._api_client = api_client

    def get_currency_rate(self, currency: str) -> dict:
        return self._api_client.get_rates(currency)