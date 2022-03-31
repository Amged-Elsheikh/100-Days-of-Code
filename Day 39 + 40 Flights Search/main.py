# %%
# # This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from notification_manager import NotificationManager
from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from datetime import datetime, timedelta
import os


day = "39 + 40"
if day not in os.getcwd():
    for folder in os.listdir():
        if day in folder:
            os.chdir(os.path.join(os.getcwd(), folder))
            del (folder, day)
            break


def date_format(date):
    return date.strftime('%d/%m/%Y')


# %%
if __name__ == '__main__':
    date_from = date_format(datetime.now() + timedelta(days=1))
    date_to = date_format(datetime.now() + timedelta(days=6*30))
    optional_queries = {
        "nights_in_dst_from": 21,
        "nights_in_dst_to": 30,
        "adults": 1,
        "selected_cabins": "M",
        "curr": "JPY",
        "limit": 20,
        "flight_type": "round",
        "sort": "quality",
    }
    data_manager = DataManager()

    fly_from = "NRT,HND"
    desired_distantions = ["AE", "DUS", "KRT", "LON"]
    for fly_to in desired_distantions:
        results = FlightSearch(fly_from, fly_to, date_from,
                               date_to, **optional_queries)
        if len(results.search_data) == 0:
            print("No flights available")
        else:
            flight_details = FlightData(results.search_data[0])
            data_manager.compare_price(
                flight_details.departure_city,
                flight_details.arrival_city,
                flight_details.price,
                flight_details.deep_link)
    data_manager.update_data()