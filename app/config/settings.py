from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    telegram_token: str

    @classmethod
    def from_env(cls) -> "Settings":
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

        if not telegram_token:
            raise ValueError("Environment variable TELEGRAM_BOT_TOKEN is not set")

        return cls(telegram_token=telegram_token)