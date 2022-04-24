import csv
import os

if __name__ == "__main__":
    day = "39 + 40"
    if day not in os.getcwd():
        for path in os.listdir():
            if day in path:
                os.chdir(os.path.join(os.getcwd(), path))
    
    with open('users.csv', 'a') as csv_file:
        fieldnames = ["First Name", "Last Name", "Email"]
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        first_name = input("Write your first name: ")
        last_name = input("Write your last name: ")
        email = input("Write your email address: ")
        info = {
            "First Name": first_name,
            "Last Name": last_name,
            "Email": email
        }
        csv_writer.writerow(info)
