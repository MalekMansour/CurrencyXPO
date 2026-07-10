# 💱 CurrencyXPO

A modern Python desktop application for monitoring live currency exchange rates, performing currency conversions, and managing personal financial records through a futuristic, terminal-inspired interface.

---

## 📝 Overview

**CurrencyXPO** is a financial dashboard built with Python, CustomTkinter, and the ExchangeRate API. It combines real-time exchange rate data with an interactive cyber-themed interface that allows users to:

* **Convert currencies instantly** across dozens of international options.
* **View live exchange rate updates** via a dedicated status console.
* **Track purchases and expenses** in multiple currencies.
* **Create financial savings goals** and monitor progress.
* **Browse a scrolling market ticker** reminiscent of a stock-market display.
* **Highlight specific currencies** within conversion results for rapid comparison.

> 💡 **Offline Mode:** The application automatically falls back to simulated market data whenever an internet connection is unavailable, ensuring uninterrupted uptime.

---

## ⚡ Features

### 💵 Live Currency Exchange & Converter
* **Real-Time Data:** Fetches live exchange rates directly from the ExchangeRate API.
* **Multi-Attribute Search:** Quickly filter and find currencies by currency code, country name, or currency name.
* **Conversion Matrix:** Convert an amount and instantly view its value across every available currency at once.
* **Highlight System:** Quickly isolate specific currencies inside the conversion matrix for easier comparison.
  * *Example filter:* `usd cad eur jpy`

### 📊 Live Market Feed & Ticker
* **Scrolling Ticker:** A continuous, stock-market style ticker displaying baseline rates.
* **Animated Console:** A live-updating market feed that displays simulated price movements, complete with:
  * Currency pairs & timestamps.
  * Real-time exchange values.
  * Percentage fluctuations with color-coded market direction indicators.

### 📉 Financial Management
* **Expense Tracker:** Log everyday purchases by item description, amount, and currency.
* **Savings Vault:** Define and fund custom financial goals (e.g., *Vacation, New PC, Car, Emergency Fund*) and track your targets.

### 🎨 Cyber Terminal Interface
* **Matrix-Inspired Aesthetics:** Sleek dark mode interface paired with high-contrast UI elements.
* **Visual Telemetry:** Neon green financial highlights for gains/selections and sharp red indicators for market losses.
* **Multi-Threaded Performance:** Smooth, responsive UI animation driven by background execution.

---

## 🛠️ Technologies Used

| Category | Technology / Library |
| :--- | :--- |
| **Language** | Python 3 |
| **GUI Framework** | CustomTkinter, Tkinter |
| **Networking** | Requests |
| **Concurrency** | Threading |
| **Data & Logic** | ExchangeRate API, Random, Time |

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/MalekMansour/CurrencyXPO.git](https://github.com/MalekMansour/CurrencyXPO.git)
   cd CurrencyXPO
