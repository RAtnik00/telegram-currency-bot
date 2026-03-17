from decimal import Decimal
import requests

from app.clients.base import CurrencyRatesProvider
from app.models.currency_rate import CurrencyRate, RateType

class CurrencyApiClient(CurrencyRatesProvider):
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

    def get_rate(
            self,
            base_currency: str,
            target_currency: str,
            rate_type: RateType = "general",
    ) -> CurrencyRate | None:
        try:
            rates = self.get_latest_rates(
                base=base_currency,
                symbols=[target_currency],
            )

            if not rates:
                return None

            rate_value = rates.get(target_currency.upper())
            if rate_value is None:
                return None

            return CurrencyRate(
                base_currency=base_currency.upper(),
                target_currency=target_currency.upper(),
                rate_type="general",
                value=Decimal(str(rate_value)),
                source="frankfurter",
            )
        except requests.RequestException as error:
            print(f"[CurrencyApiClient] request error: {error}")
            return None
        except (ValueError, TypeError) as error:
            print(f"[CurrencyApiClient] data error: {error}")
            return None