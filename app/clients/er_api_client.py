from decimal import Decimal

import requests

from app.clients.base import CurrencyRatesProvider
from app.models.currency_rate import CurrencyRate, RateType


class ErApiClient(CurrencyRatesProvider):
    def __init__(self, base_url: str = "https://open.er-api.com/v6") -> None:
        self._base_url = base_url.rstrip("/")

    def get_latest_rates(
        self,
        base: str,
        symbols: list[str] | None = None,
    ) -> dict[str, float] | None:
        response = requests.get(
            f"{self._base_url}/latest/{base.upper()}",
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()

        if data.get("result") != "success":
            return None

        rates = data.get("rates")
        if not isinstance(rates, dict):
            return None

        if symbols:
            allowed = {symbol.upper() for symbol in symbols}
            return {
                code: value
                for code, value in rates.items()
                if code.upper() in allowed
            }

        return rates

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
                source="er-api",
            )
        except requests.RequestException as error:
            print(f"[ErApiClient] request error: {error}")
            return None
        except (ValueError, TypeError) as error:
            print(f"[ErApiClient] data error: {error}")
            return None