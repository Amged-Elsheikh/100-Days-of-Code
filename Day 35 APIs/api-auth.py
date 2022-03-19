import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

OPEN_WEATHER_MAP_API = os.getenv("OPEN_WEATHER_MAP_API")

def send_SMS():
    account_sid = 'ACfde611c58638a773bfc75fc71f920d53'
    auth_token = os.getenv("TWILIO_TOKEN")
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body = "Check the weather status",
        from_ = '+19036272805',
        to = '+818062529513'
    )


TIME_CHECKING_LENGTH=14  # hours
url="http://api.openweathermap.org/data/2.5/onecall"
parameters={"lon": 140.8443875228813,
              "lat": 38.25452949320056,
              "appid": OPEN_WEATHER_MAP_API,
              "units": "metric",
              "exclude": 'current,minutely,daily'
              }

r = requests.get(url, params=parameters)
data = r.json()
hourly_data = data["hourly"][:TIME_CHECKING_LENGTH]

hourly_weather_state = [i["weather"][0]["id"] for i in hourly_data]

warnings_count = len(
    list(filter(lambda x: x < 700, hourly_weather_state)))

if warnings_count >= 3:  # Rain or Snow for three hours or more
    print(f'Current weather is {hourly_data[0]["weather"][0]["main"]}')
    # send_SMS()
    print("DONE!")
else:
    pass
