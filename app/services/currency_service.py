from decimal import Decimal

from app.clients.base import CurrencyRatesProvider
from app.models.currency_rate import CurrencyRate, RateType


class CurrencyService:
    def __init__(
        self,
        general_rates_provider: CurrencyRatesProvider,
        cash_rates_provider: CurrencyRatesProvider | None = None,
    ) -> None:
        self._general_rates_provider = general_rates_provider
        self._cash_rates_provider = cash_rates_provider

    def get_rate(
        self,
        base_currency: str,
        target_currency: str,
        rate_type: RateType = "general",
    ) -> CurrencyRate | None:
        base_currency = base_currency.upper()
        target_currency = target_currency.upper()

        if base_currency == target_currency:
            return CurrencyRate(
                base_currency=base_currency,
                target_currency=target_currency,
                rate_type=rate_type,
                value=Decimal("1"),
                source="internal",
            )

        provider = self._select_provider(rate_type)
        if provider is None:
            return None

        return provider.get_rate(
            base_currency=base_currency,
            target_currency=target_currency,
            rate_type=rate_type,
        )

    def convert(
        self,
        amount: Decimal,
        base_currency: str,
        target_currency: str,
        rate_type: RateType = "general",
    ) -> Decimal | None:
        rate = self.get_rate(
            base_currency=base_currency,
            target_currency=target_currency,
            rate_type=rate_type,
        )

        if rate is None:
            return None

        return amount * rate.value

    def _select_provider(
        self,
        rate_type: RateType,
    ) -> CurrencyRatesProvider | None:
        if rate_type == "general":
            return self._general_rates_provider

        if rate_type in ("buy", "sell"):
            if self._cash_rates_provider is not None:
                return self._cash_rates_provider

            return self._general_rates_provider

        return self._general_rates_provider