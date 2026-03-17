from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

RateType = Literal["general", "buy", "sell"]

@dataclass(slots=True, frozen=True)
class CurrencyRate:
    base_currency: str
    target_currency: str
    rate_type: RateType
    value: Decimal
    source: str