from typing import Protocol
from app.models.currency_rate import CurrencyRate, RateType

class CurrencyRatesProvider(Protocol):
    def get_rate(
            self,
            base_currency: str,
            target_currency: str,
            rate_type: RateType = "general",
    ) -> CurrencyRate | None:
        pass