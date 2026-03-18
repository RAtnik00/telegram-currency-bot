from decimal import Decimal, ROUND_HALF_UP

from app.clients.base import CurrencyRatesProvider
from app.models.currency_rate import CurrencyRate, RateType


class SimulatedCashRatesClient(CurrencyRatesProvider):
    def __init__(
        self,
        general_rates_provider: CurrencyRatesProvider,
        spread_percent: Decimal = Decimal("0.5"),
    ) -> None:
        self._general_rates_provider = general_rates_provider
        self._spread_percent = spread_percent

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

        general_rate = self._general_rates_provider.get_rate(
            base_currency=source_currency,
            target_currency=destination_currency,
            rate_type="general",
        )

        if general_rate is None:
            return None

        multiplier = self._get_multiplier(rate_type)
        simulated_value = (general_rate.value * multiplier).quantize(
            Decimal("0.0001"),
            rounding=ROUND_HALF_UP,
        )

        return CurrencyRate(
            base_currency=source_currency,
            target_currency=destination_currency,
            rate_type=rate_type,
            value=simulated_value,
            source="simulated_cash",
        )

    def _get_multiplier(self, rate_type: RateType) -> Decimal:
        spread_ratio = self._spread_percent / Decimal("100")

        if rate_type == "buy":
            return Decimal("1") - spread_ratio

        return Decimal("1") + spread_ratio