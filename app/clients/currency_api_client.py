import requests


class CurrencyApiClient:
    def __init__(self, base_url: str = "https://api.frankfurter.app") -> None:
        self._base_url = base_url

    def get_rates(self, base_currency: str) -> dict[str, float]:
        response = requests.get(
            f"{self._base_url}/latest",
            params={"base": base_currency.upper()},
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        return data.get("rates", {})

    def get_latest_rates(
        self,
        base: str,
        symbols: list[str] | None = None,
    ) -> dict[str, float] | None:
        params = {"base": base.upper()}

        if symbols:
            params["symbols"] = ",".join(symbol.upper() for symbol in symbols)

        response = requests.get(
            f"{self._base_url}/latest",
            params=params,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        return data.get("rates")