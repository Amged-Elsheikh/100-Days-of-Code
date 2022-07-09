import pandas as pd
import os
from flight_data import FlightData


class DataManager:
    """This class is responsible for working with the csv file.
    It can compare current price with old price, update the csv file and delete destinations
    """

    def __init__(self):
        try:
            self.data = pd.read_csv("flight_data.csv", header=0)
        except:
            day = "39 + 40"
            if day not in os.getcwd():
                for path in os.listdir():
                    if day in path:
                        os.chdir(os.path.join(os.getcwd(), path))
                        self.data = pd.read_csv("flight_data.csv", header=0)
                        break

    def compare_price(self, flight_details: FlightData):

        from_ = flight_details.departure_city
        to = flight_details.arrival_city
        departure_date = flight_details.departure_date
        return_arrival = flight_details.return_arrival
        new_price = flight_details.price
        new_link = flight_details.deep_link

        # Check for old price if any
        update_condition = (self.data["From"] == from_) & (
            self.data['To'] == to)
        compared_row = self.data.loc[update_condition]
        # In case of new flight
        if len(compared_row) == 0:
            self.data.loc[len(self.data)] = [from_, to, new_price,
                                             departure_date, return_arrival, new_link]
        else:
            if compared_row["Price"].values[0] > new_price:
                columns = ['Price', "Department date", "Return date", "Link"]
                updated_data = [new_price, departure_date,
                                return_arrival, new_link]
                # Update exisiting data
                self.data[columns].loc[update_condition] = updated_data

    def update_data(self):
        self.data.to_csv("flight_data.csv", index=False)

    def delete_dist(self, dist):
        self.data.drop(
            self.data.loc[self.data["To"] == dist].index, inplace=True)
