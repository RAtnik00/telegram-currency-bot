from app.clients.base import CurrencyRatesProvider
from app.models.currency_rate import CurrencyRate, RateType


class FallbackCurrencyClient(CurrencyRatesProvider):
    def __init__(
        self,
        primary_provider: CurrencyRatesProvider,
        secondary_provider: CurrencyRatesProvider,
    ) -> None:
        self._primary_provider = primary_provider
        self._secondary_provider = secondary_provider

    def get_rate(
        self,
        base_currency: str,
        target_currency: str,
        rate_type: RateType = "general",
    ) -> CurrencyRate | None:
        primary_rate = self._primary_provider.get_rate(
            base_currency=base_currency,
            target_currency=target_currency,
            rate_type=rate_type,
        )
        if primary_rate is not None:
            return primary_rate

        return self._secondary_provider.get_rate(
            base_currency=base_currency,
            target_currency=target_currency,
            rate_type=rate_type,
        )