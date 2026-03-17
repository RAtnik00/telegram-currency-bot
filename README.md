# 💱 Telegram Currency Bot

A Telegram bot for currency conversion built with **aiogram v3**, supporting real-time exchange rates and different operation types (**general / buy / sell**).

---

## 🚀 Features

- 🔄 Currency conversion (USD, EUR, PLN, GBP, etc.)
- 📊 Real-time exchange rates
- 💰 Support for different operation types:
  - `general` — market/reference rate
  - `buy` — bank buy rate
  - `sell` — bank sell rate
- ⚡ Fast responses with caching
- 🧠 FSM-based user flow (aiogram v3)
- 🧩 Clean architecture:
  - handlers → services → clients → cache → validators

---

## 🏗️ Architecture

```
handlers
   ↓
services
   ↓
clients (API)
   ↓
cache
```

### API Providers

- **Frankfurter API**
  - Used for `general` rates
  - Source: https://api.frankfurter.app

- **NBP API (Poland)**
  - Used for `buy` / `sell` rates
  - Source: https://api.nbp.pl

---

## 🛠️ Tech Stack

- Python 3.12+
- aiogram v3
- requests
- dotenv
- Decimal (for precise calculations)

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/your-username/telegram-currency-bot.git
cd telegram-currency-bot
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

---

## ▶️ Run the bot

```bash
python -m app.main
```

---

## 🤖 Bot Commands

- `/start` — start the bot
- `/rate USD` — get exchange rates for currency
- Conversion flow:
  1. Select base currency
  2. Select target currency
  3. Choose operation type (buy/sell/general)
  4. Enter amount

---

## 💡 Example

```
100 USD → PLN

Result:
367.94 PLN
Mode: sell
```

---

## 📦 Project Structure

```
app/
├── bot/
│   ├── handlers/
│   ├── states/
│
├── services/
│   └── currency_service.py
│
├── clients/
│   ├── currency_api_client.py
│   ├── nbp_buy_rates_client.py
│   ├── nbp_sell_rates_client.py
│
├── cache/
├── validators/
├── models/
│
└── main.py
```

---

## 🧠 Key Concepts

### FSM (Finite State Machine)
Used to guide user through conversion steps:
- select currency
- select operation type
- enter amount

### Clean Architecture
- Handlers do NOT contain business logic
- Services manage logic
- Clients handle external APIs

### Decimal instead of float
Used for accurate financial calculations:

```python
from decimal import Decimal
```

---

## 🔮 Future Improvements

- 🔍 Currency search
- ⭐ Favorite currency pairs
- 🔁 Swap currencies button
- 📜 Conversion history
- 🌐 Async HTTP (httpx)
- 🧪 Unit tests

---

## 👨‍💻 Author

Dmitry Yaremenko

