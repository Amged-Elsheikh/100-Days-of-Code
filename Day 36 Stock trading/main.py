import os
import smtplib
import requests
from dotenv import load_dotenv
load_dotenv()

MY_EMAIL = os.getenv('MY_EMAIL')
PASSWORD = os.getenv('PASSWORD')
COIN_MARKET_API = os.getenv("alphavantage_API")
NEWS_API = os.getenv("NEWS_API")


def get_coins_data(coins: dict) -> dict:
    """
    coins is a dict. Coin symbol is the key, coin name is the corresponding value for the key. The symbol used to get market data, and name is used to get the latest news.

    output data is a dict. coin symbol is the key, coin market data is the corresponding value for the coin.
    """
    data = dict()
    for coin in coins.keys():
        url = 'https://www.alphavantage.co/query?'
        params = {"function": "CRYPTO_INTRADAY",
                  "symbol": coin,
                  "market": "USD",
                  "interval": "60min",
                  "apikey": COIN_MARKET_API}
        r = requests.get(url, params=params)
        r.raise_for_status()
        data[coin] = r.json()['Time Series Crypto (60min)']
        # Retrived data are in GMT
    return data


def get_latest_news(coin_name: str, news_count: int) -> list:
    news_url = "https://newsapi.org/v2/everything?"

    news_params = {"q": coin_name,
                   "language": "en",
                   "sortBy": "publishedAt"}

    headers = {"Authorization": NEWS_API}

    r = requests.get(news_url, news_params, headers=headers)
    r.raise_for_status()
    news_data = r.json()['articles'][:news_count]
    return news_data


def send_email(message: str) -> None:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        # Secure the connection
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="amgedelshiekh@gmail.com",
                            msg=message)

                            
def track_coin(Coins: dict, comparing_period=24, trigger_percent=0.08, news_count=3):
    data = get_coins_data(Coins)
    for coin in Coins.keys():
        coin_data = data[coin]
        # Get current closing price
        hours_key = list(coin_data.keys())
        last_close_price = float(coin_data[hours_key[0]]["4. close"])
        # Compare with previous (n-hours) closing prices
        for i in range(1, comparing_period+1):
            previous_close_price = float(coin_data[hours_key[i]]["4. close"])
            # Get percentage change
            percentage_change = (previous_close_price -
                                 last_close_price)/previous_close_price
            # Send informations if absolute change value goes above the trigger
            if abs(percentage_change) >= trigger_percent:
                # For positive Change
                message = f"Subject:{coin} has a Rapid Move!!\n\n"
                
                if percentage_change > 0:
                    message += f"{coin} price goes up to {last_close_price}$ with change {percentage_change*100:.2f}% compares to the last {i} hours.\n\n News:\n"
                else:
                    message += f"{coin} price goes down to {last_close_price}$ with change {percentage_change*100:.2f}% compares to the last {i} hours.\n\nNews:\n"

                coin_name = Coins[coin]
                news_data = get_latest_news(coin_name, news_count)
                for news in news_data:
                    news_title = news["title"]
                    news_url = news["url"]
                    message += f"{news_title}\n{news_url}\n\n"
                # Exit the coin loop, so we won't have duplicate emails.
                break
        send_email(message)


if __name__ == "__main__":
    Coins = {"ADA": "cardano", "LUNA": "terra luna"}
    track_coin(Coins, comparing_period=24, trigger_percent=0.01, news_count=3)
