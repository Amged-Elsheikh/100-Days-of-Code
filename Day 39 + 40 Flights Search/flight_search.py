from dotenv import load_dotenv
import os
import requests
load_dotenv()


class FlightSearch:
    flight_search_endpoint = "https://tequila-api.kiwi.com/v2/search"

    def __init__(self, fly_from: str, fly_to: str,
                 date_from: str, date_to: str, **kwargs):
        """This class will talk with the API to get all flights information.
        For all allowed keywords, check https://tequila.kiwi.com/portal/docs/tequila_api/search_api
        """
        self.fly_from = fly_from
        self.fly_to = fly_to
        self.date_from = date_from
        self.date_to = date_to
        self.__dict__.update(kwargs)
        self.__search()

    def __search(self):
        _flight_search_headers = {"apikey": os.environ.get('Tequila_API')}
        self.response = requests.get(self.flight_search_endpoint,
                                headers=_flight_search_headers,
                                params=self.__dict__)
        self.response.raise_for_status()
        self.search_data = self.response.json()['data']
