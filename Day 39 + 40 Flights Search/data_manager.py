import pandas as pd
import os


class DataManager:
    # This class is responsible for working with the csv file.
    def __init__(self):
        try:
            self.data = pd.read_csv("flight_data.csv", header=0)
        except:
            day = "39 + 40"
            if day not in os.getcwd():
                for folder in os.listdir():
                    if day in folder:
                        os.chdir(os.path.join(os.getcwd(), folder))
                        self.data = pd.read_csv("flight_data.csv", header=0)
                        break

    def compare_price(self, from_, to, new_price, new_link):
        compare_row = self.data.loc[(
            self.data["From"] == from_) & (self.data['To'] == to)]
        if len(compare_row) == 0:
            self.data.loc[len(self.data)] = [from_, to, new_price, new_link]
        else:
            if compare_row["Price"].values[0] > new_price:

                self.data[['Price', "Link"]].loc[(self.data["From"] == from_) & (
                    self.data['To'] == to)] = [new_price, new_link]

    def update_data(self):
        self.data.to_csv("flight_data.csv", index=False)

    def delete_dist(self, dist):
        self.data.drop(self.data.loc[d.data["To"] == dist].index, inplace=True)
