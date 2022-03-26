class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, flight_data):
        self.flight_data = flight_data
        self.price = flight_data['price']
        self.currency = list(flight_data['conversion'].keys())[-1]
        self.departure_airport = flight_data['flyFrom']
        self.departure_city = flight_data['cityFrom']
        self.arrival_airport = flight_data['flyTo']
        self.arrival_city = flight_data['cityTo']
        self.stay_lengthen = flight_data['nightsInDest']
        self.fare_details = flight_data['fare']
        self.website_entry = flight_data['deep_link']
        self.route = flight_data['route']
        self.flight_date = self.route[0]['local_departure']
        self.return_arrival = self.route[-1]['local_arrival']
        self.deep_link = flight_data['deep_link']
    
    @property
    def link(self):
        import webbrowser
        webbrowser.open_new_tab(self.flight_data['deep_link'])