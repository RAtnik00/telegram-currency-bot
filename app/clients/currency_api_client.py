import requests


class CurrencyApiClient:
    BASE_URL = "https://api.frankfurter.dev/v1"

    def get_rates(self, base_currency: str) -> dict:
        url = f"{self.BASE_URL}/latest"
        params = {"base": base_currency.upper()}

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        return data.get("rates", {})