from app.cache.currency_cache import CurrencyCache
from app.clients.currency_api_client import CurrencyApiClient


class CurrencyService:
    def __init__(
        self,
        api_client: CurrencyApiClient,
        cache: CurrencyCache | None = None,
    ) -> None:
        self._api_client = api_client
        self._cache = cache or CurrencyCache()

    def get_currency_rate(self, currency: str) -> dict[str, float] | None:
        base_currency = currency.upper()
        cache_key = f"rates:{base_currency}:EUR,GBP,PLN"

        cached_rates = self._cache.get(cache_key)
        if cached_rates is not None:
            return cached_rates

        rates = self._api_client.get_latest_rates(
            base=base_currency,
            symbols=["EUR", "GBP", "PLN"],
        )

        if rates:
            self._cache.set(cache_key, rates)

        return rates

    def convert_currency(
        self,
        amount: float,
        from_currency: str,
        to_currency: str,
    ) -> float | None:
        if amount <= 0:
            return None

        source_currency = from_currency.upper()
        target_currency = to_currency.upper()

        if source_currency == target_currency:
            return amount

        cache_key = f"convert:{source_currency}:{target_currency}"

        cached_rates = self._cache.get(cache_key)
        if cached_rates is not None:
            rate = cached_rates.get(target_currency)
            if rate is not None:
                return amount * rate

        rates = self._api_client.get_latest_rates(
            base=source_currency,
            symbols=[target_currency],
        )

        if not rates:
            return None

        self._cache.set(cache_key, rates)

        rate = rates.get(target_currency)
        if rate is None:
            return None

        return amount * rate