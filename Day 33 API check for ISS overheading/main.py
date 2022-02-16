from datetime import datetime
from time import sleep
import requests
import smtplib


def process_time(sun):
    sun = sun.split("T")
    sun = sun[1].split(":")
    hr = int(sun[0]) + 9  # All times are in UTC while my timezone is JST
    if hr >= 24:
        hr -= 24
    return hr


def is_night(my_lat, my_lng):
    parameters = {"lat": my_lat,
                  "lng": my_lng,
                  "formatted": 0
                  }

    r = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    r.raise_for_status()
    response = r.json()
    sunrise = process_time(response["results"]["sunrise"])  # 6
    sunset = process_time(response["results"]["sunset"])  # 17

    if sunset > sunrise:
        day_hrs = [i for i in range(sunrise, sunset+1)]
    elif sunset < sunrise:
        day_hrs = [i for i in range(sunset, sunrise+1)]
    elif sunset == sunrise:
        day_hrs = [sunset]
    time_now = datetime.now().hour
    if time_now in day_hrs:
        return False
    else:
        return True


def is_iss_overhead(my_lat, my_lng, e=5):
    r = requests.get("http://api.open-notify.org/iss-now.json")
    r.raise_for_status()
    response = r.json()
    iss_lat = float(response["iss_position"]["latitude"])
    iss_lng = float(response["iss_position"]["longitude"])

    if (iss_lat-e) <= my_lat <= (iss_lat+e) and (iss_lng-e) <= my_lng <= (iss_lng+e):
        return True
    else:
        return False


if __name__ == "__main__":
    my_lat = 38.282925
    my_lng = 140.851259
    my_email = ""
    my_password = ""

    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(my_email, my_password)

    while True:
        if is_night(my_lat, my_lng) and is_iss_overhead(my_lat, my_lng):
            connection.sendmail(from_addr=my_email, to_addrs=my_email,
                                msg="Subject:ISS is overhead\n\nISS is overheading you, LOOOK AT THE SKY")
            sleep(3*60*60)  # sleep for 3 hrs
        else:
            sleep(10*60)  # check every 10 min
