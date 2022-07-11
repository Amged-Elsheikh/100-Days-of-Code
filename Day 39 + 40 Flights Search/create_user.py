import os
import re

import pandas as pd

if __name__ == "__main__":
    day = "39 + 40"
    if day not in os.getcwd():
        for path in os.listdir():
            if day in path:
                os.chdir(os.path.join(os.getcwd(), path))


class User:

    def __init__(self):
        self.first_name = input("Write your first name: ")
        self.last_name = input("Write your last name: ")
        while True:
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            self.email = input("Write your email address: ")
            if re.fullmatch(regex, self.email):
                break
            else:
                print("\nWrong email adress.")


    def add_user(self):
        file = pd.read_csv("users.csv")
        # Check if the email is used
        duplicated = file.loc[file['Email'] == self.email]
        # When the email is new
        if not bool(len(duplicated)):
            data = {'First Name': self.first_name,
                    "Last Name": self.last_name,
                    'Email': self.email}

            file = file.append(data, ignore_index=True)
            file.to_csv("users.csv", index=False)
        if bool(len(duplicated)):
            check = input("Email is already used, do you want to update information?[Y/N]\n")
            if check.lower()=="n":
                pass
            elif check.lower()=="y":
                file[duplicated] = [self.first_name, self.last_name, self.email]
            else:
                print(f"User inputed {check}. Please input [y/n].\n")
                self.add_user()

if __name__ == '__main__':
    a = User()
    a.add_user()
