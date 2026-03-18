from decimal import Decimal

from app.cache.currency_cache import CurrencyCache
from app.clients.base import CurrencyRatesProvider
from app.models.currency_rate import CurrencyRate, RateType


class CurrencyService:
    def __init__(
        self,
        general_rates_provider: CurrencyRatesProvider,
        cash_rates_provider: CurrencyRatesProvider | None = None,
        cache: CurrencyCache | None = None,
    ) -> None:
        self._general_rates_provider = general_rates_provider
        self._cash_rates_provider = cash_rates_provider
        self._cache = cache or CurrencyCache()

    def get_rate(
            self,
            base_currency: str,
            target_currency: str,
            rate_type: RateType = "general",
    ) -> CurrencyRate | None:
        source_currency = base_currency.upper()
        destination_currency = target_currency.upper()

        if source_currency == destination_currency:
            return CurrencyRate(
                base_currency=source_currency,
                target_currency=destination_currency,
                rate_type=rate_type,
                value=Decimal("1"),
                source="internal",
            )

        cache_key = f"rate:{rate_type}:{source_currency}:{destination_currency}"
        cached_rate = self._cache.get(cache_key)
        if cached_rate is not None:
            return cached_rate

        general_rate = self._general_rates_provider.get_rate(
            base_currency=source_currency,
            target_currency=destination_currency,
            rate_type="general",
        )

        if general_rate is None:
            return None

        rate = general_rate

        if rate_type == "buy":
            rate = CurrencyRate(
                base_currency=source_currency,
                target_currency=destination_currency,
                rate_type="buy",
                value=general_rate.value * Decimal("0.995"),
                source="simulated_buy",
            )
        elif rate_type == "sell":
            rate = CurrencyRate(
                base_currency=source_currency,
                target_currency=destination_currency,
                rate_type="sell",
                value=general_rate.value * Decimal("1.005"),
                source="simulated_sell",
            )
        else:
            rate = CurrencyRate(
                base_currency=source_currency,
                target_currency=destination_currency,
                rate_type="general",
                value=general_rate.value,
                source=general_rate.source,
            )

        self._cache.set(cache_key, rate)
        return rate

    def convert_currency(
        self,
        amount: Decimal,
        from_currency: str,
        to_currency: str,
        rate_type: RateType = "general",
    ) -> Decimal | None:
        if amount <= 0:
            return None

        rate = self.get_rate(
            base_currency=from_currency,
            target_currency=to_currency,
            rate_type=rate_type,
        )

        if rate is None:
            return None

        return amount * rate.value

    def get_currency_rate(self, currency: str) -> dict[str, dict[str, Decimal]] | None:
        base_currency = currency.upper()
        symbols = ["EUR", "GBP", "PLN"]
        result: dict[str, dict[str, Decimal]] = {}

        for target_currency in symbols:
            if target_currency == base_currency:
                continue

            general_rate = self.get_rate(
                base_currency=base_currency,
                target_currency=target_currency,
                rate_type="general",
            )
            buy_rate = self.get_rate(
                base_currency=base_currency,
                target_currency=target_currency,
                rate_type="buy",
            )
            sell_rate = self.get_rate(
                base_currency=base_currency,
                target_currency=target_currency,
                rate_type="sell",
            )

            if general_rate is None and buy_rate is None and sell_rate is None:
                continue

            result[target_currency] = {}

            if general_rate is not None:
                result[target_currency]["general"] = general_rate.value
            if buy_rate is not None:
                result[target_currency]["buy"] = buy_rate.value
            if sell_rate is not None:
                result[target_currency]["sell"] = sell_rate.value

        return result or None

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