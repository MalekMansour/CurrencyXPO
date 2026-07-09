# 💱 CurrencyXPO

A modern Python desktop application for monitoring live currency exchange rates, performing currency conversions, and managing personal financial records through a futuristic terminal-inspired interface.

## Overview

CurrencyXPO is a financial dashboard built with Python, CustomTkinter, and the ExchangeRate API. It combines real-time exchange rate data with an interactive cyber-themed interface that allows users to:

* Convert currencies instantly
* View live exchange rate updates
* Track purchases and expenses
* Create financial savings goals
* Browse a scrolling market ticker
* Highlight specific currencies in conversion results

The application automatically falls back to simulated market data whenever an internet connection is unavailable.

⸻

## Features

- Live Currency Exchange

* Fetches real-time exchange rates from the ExchangeRate API
* Supports dozens of international currencies
* Automatic fallback to offline simulation mode

- Currency Converter

* Convert any amount between supported currencies
* Search currencies by:
    * Currency code
    * Country code
    * Currency name
* View conversions to every available currency at once

- Highlight System

Quickly highlight selected currencies inside the conversion matrix.

Example:

usd cad eur jpy

The matching currencies will be highlighted for easier comparison.

⸻

📈 Live Market Feed

A continuously updating market console displays simulated price movements including:

* Currency
* Timestamp
* Exchange value
* Percentage increase/decrease
* Color-coded market direction

⸻

💰 Expense Tracker

Record purchases including:

* Item description
* Amount
* Currency

Example:

Laptop
1200 CAD

⸻

🎯 Savings Vault

Create financial goals such as:

* Vacation
* New PC
* Car
* Emergency Fund

Store target values and monitor your objectives.

⸻

📊 Scrolling Currency Ticker

A live ticker continuously displays exchange rates for multiple currencies in a stock-market style display.

⸻

🖥️ Interface

CurrencyXPO features a cyber-inspired terminal aesthetic including:

* Dark Mode Interface
* Neon Green Financial Highlights
* Red Loss Indicators
* Animated Market Feed
* Live Status Console
* Matrix-style Dashboard Layout

⸻

🛠️ Technologies Used

* Python 3
* CustomTkinter
* Tkinter
* Requests
* Threading
* ExchangeRate API
* Random
* Time

⸻

📦 Installation

Clone the repository:

git clone https://github.com/yourusername/CurrencyXPO.git

Navigate into the project:

cd CurrencyXPO

Install dependencies:

pip install customtkinter requests

Run the application:

python CurrencyXPO.py

⸻

🌐 API

CurrencyXPO retrieves exchange rates from:

https://open.er-api.com/v6/latest/USD

If the API is unavailable, the application automatically switches to locally simulated exchange data.

⸻

📂 Project Structure

CurrencyXPO/
│
├── CurrencyXPO.py
├── README.md
└── requirements.txt

⸻

🚀 Future Improvements

* Historical exchange rate charts
* Currency trend graphs
* Portfolio tracking
* Export transaction history to CSV
* Dark/Light theme toggle
* Favorite currencies
* Automatic refresh settings
* Multi-language support

⸻

📸 Screenshots

Add screenshots of your application here.

Example:

images/dashboard.png
images/converter.png
images/live-market.png

⸻

🤝 Contributing

Contributions are welcome!

If you’d like to improve CurrencyXPO, feel free to:

* Fork the repository
* Create a feature branch
* Commit your changes
* Submit a Pull Request

⸻

📄 License

This project is licensed under the MIT License.

⸻

👨‍💻 Author

Malek Mansour

Software Developer | Python • Desktop Applications • Data & Finance Tools

If you found this project helpful, consider giving it a ⭐ on GitHub!
