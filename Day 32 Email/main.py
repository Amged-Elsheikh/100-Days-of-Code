import os
from datetime import datetime
import random
import smtplib
import pandas as pd


"""
You can upload the code and all the necessary folders to pythonanywhere.com to automatically run the code everyday. Make sure to remove/comment the path changing lines of code,
"""

my_email = ""  # write your Email
password = ""  # write your password


def send_email(msg: str) -> None:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        # Secure the connection
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs="amgedelshiekh@gmail.com",
                            msg=f"Subject:Happy Birthday\n\n{msg}")


def choose_letter():
    files = os.listdir("letter_templates")
    return random.choice(files)


def is_birthday(df, name, day):
    if day.month == df.loc[name, "month"] and day.day == df.loc[name, "day"]:
        return True
    else:
        return False


# DAY = "32"
# if DAY not in os.getcwd():
#     sub_folder = list(filter(lambda x: DAY in x, os.listdir()))
#     if sub_folder:
#         os.chdir(os.path.join(os.getcwd(), sub_folder[0]))


my_name = "Amged"
df = pd.read_csv("birthdays.csv", header=0, index_col="name")
today = datetime.now()
for name in df.index:
    if is_birthday(df, name, today):
        letter_folder = choose_letter()
        with open(f"letter_templates/{letter_folder}") as f:
            letter = f.read()
        letter = letter.replace("[NAME]", name)
        letter = letter.replace("[Me]", my_name)
        print(letter)
        send_email(msg=letter)
    else:
        pass
