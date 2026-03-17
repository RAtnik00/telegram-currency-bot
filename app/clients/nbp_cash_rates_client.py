from decimal import Decimal
from typing import Any

import requests

from app.clients.base import CurrencyRatesProvider
from app.models.currency_rate import CurrencyRate, RateType


class NbpCashRatesClient(CurrencyRatesProvider):
    def __init__(self, base_url: str = "https://api.nbp.pl/api") -> None:
        self._base_url = base_url.rstrip("/")

    def get_rate(
        self,
        base_currency: str,
        target_currency: str,
        rate_type: RateType = "general",
    ) -> CurrencyRate | None:
        source_currency = base_currency.upper()
        destination_currency = target_currency.upper()

        if rate_type not in ("buy", "sell"):
            return None

        if source_currency == destination_currency:
            return CurrencyRate(
                base_currency=source_currency,
                target_currency=destination_currency,
                rate_type=rate_type,
                value=Decimal("1"),
                source="nbp",
            )

        try:
            table = self._get_table_c()
        except requests.RequestException as error:
            print(f"[NbpCashRatesClient] request error: {error}")
            return None
        except (ValueError, TypeError, KeyError) as error:
            print(f"[NbpCashRatesClient] data error: {error}")
            return None

        value = self._build_cross_rate(
            table=table,
            base_currency=source_currency,
            target_currency=destination_currency,
        )

        if value is None:
            return None

        return CurrencyRate(
            base_currency=source_currency,
            target_currency=destination_currency,
            rate_type=rate_type,
            value=value,
            source="nbp",
        )

    def _get_table_c(self) -> dict[str, dict[str, Decimal]]:
        response = requests.get(
            f"{self._base_url}/exchangerates/tables/C/",
            params={"format": "json"},
            timeout=10,
        )
        response.raise_for_status()

        payload = response.json()
        if not payload or not isinstance(payload, list):
            raise ValueError("NBP API returned invalid payload.")

        rates = payload[0].get("rates")
        if not rates or not isinstance(rates, list):
            raise ValueError("NBP API returned empty rates table.")

        result: dict[str, dict[str, Decimal]] = {}
        for item in rates:
            code = str(item["code"]).upper()
            bid = Decimal(str(item["bid"]))
            ask = Decimal(str(item["ask"]))

            result[code] = {
                "bid": bid,
                "ask": ask,
            }

        return result

    def _build_cross_rate(
        self,
        table: dict[str, dict[str, Decimal]],
        base_currency: str,
        target_currency: str,
    ) -> Decimal | None:
        source_to_pln = self._get_to_pln_rate(
            table=table,
            currency=base_currency,
        )
        if source_to_pln is None:
            return None

        pln_to_target = self._get_from_pln_rate(
            table=table,
            currency=target_currency,
        )
        if pln_to_target is None:
            return None

        return source_to_pln / pln_to_target

    def _get_to_pln_rate(
        self,
        table: dict[str, dict[str, Decimal]],
        currency: str,
    ) -> Decimal | None:
        if currency == "PLN":
            return Decimal("1")

        data = table.get(currency)
        if data is None:
            return None

        return data["bid"]

    def _get_from_pln_rate(
        self,
        table: dict[str, dict[str, Decimal]],
        currency: str,
    ) -> Decimal | None:
        if currency == "PLN":
            return Decimal("1")

        data = table.get(currency)
        if data is None:
            return None

        return data["ask"]