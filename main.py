import sqlite3
import requests
import time
from datetime import datetime

DB_NAME = "stock_data.db"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def insert_to_db(symbol, price):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO stock_prices (symbol, price) VALUES (?, ?)",
                (symbol, price),
            )
        print(f"Successfully saved {symbol} to Database")
    except Exception as e:
        print(f"Database Error: {e}")


def get_stock_price(stock_symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_symbol}"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        return price
    except Exception as e:
        print(f"Error fetching {stock_symbol}: {e}")
        return None


TARGET_SYMBOL = "NVDA"

while True:
    price = get_stock_price(TARGET_SYMBOL)

    if price:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{now} {TARGET_SYMBOL}: {price}")
        insert_to_db(TARGET_SYMBOL, price)
    else:
        print(f"Skipping {TARGET_SYMBOL} due to error...")

    print("-" * 30)
    time.sleep(5)