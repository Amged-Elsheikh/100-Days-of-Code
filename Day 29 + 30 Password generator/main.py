# --------------- Import libraries and set working directory ----------------- #
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
from PIL import Image, ImageTk
import string
import random
from numpy import tile
import pyperclip
import json

if "29" not in os.getcwd():
    sub_folder = list(filter(lambda x: "29" in x, os.listdir()))
    if sub_folder:
        os.chdir(os.path.join(os.getcwd(), sub_folder[0]))

PASSWORD_LENGTH = 18
# ------------------------- PASSWORD GENERATOR ---------------------------- #


def generate_password(event=None):
    password_entry.delete(0, END)
    letters = list(string.ascii_lowercase +
                   string.ascii_uppercase + string.digits)
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    letters_length = random.randint(13, 16)
    symbols_length = PASSWORD_LENGTH - letters_length

    password_letters = [random.choice(letters) for _ in range(letters_length)]
    password_symbols = [random.choice(symbols) for _ in range(symbols_length)]
    password = password_letters + password_symbols
    random.shuffle(password)
    password = "".join(password)
    password_entry.insert(0, password)
# ---------------------------- SEARCH PASSWORD ------------------------------- #


def search_passwords():
    website_name = website_entry.get().title()
    try:
        with open("passwords_data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        message = "Password folder is not created yet"
        title = "Warning"
        messagebox.showwarning(title=title, message=message)
    else:
        if website_name in data.keys():
            user = data[website_name]["User"]
            password = data[website_name]["Password"]
            title = f"{website_name} Log In data"
            message = f"User name: {user}\nPassword: {password}"
            messagebox.showinfo(title=title, message=message)
        else:
            message = f"You do not have account in '{website_name}'"
            title = "Warning"
            messagebox.showwarning(title=title, message=message)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data(event=None):
    webpage = website_entry.get().title()
    user = user_entry.get()
    password = password_entry.get()
    text = f"{webpage} | {user} | {password}\n"
    warning = ""
    # Check for correct entries
    if len(webpage) < 1 or len(user) < 1 or len(password) < 8:
        if len(webpage) < 1:
            warning = f"{warning}No webpage name found.\n"
        if len(user) < 1:
            warning = f"{warning}No user name found.\n"
        if len(password) < 7:
            warning = f"{warning}Password should have 8 characters at least, but only {len(password)} provided.\n"
        messagebox.showerror(title="ERROR", message=warning)
    else:
        message = f"Website name: {webpage}\nUser: {user}\nPassword: {password}\nDo you want to continue?"
        is_ok = messagebox.askokcancel(title="Confirmation", message=message)
        if is_ok:
            new_data = {webpage: {"User": user, "Password": password}}
            update_websites_list(
                new_data=new_data, file_name="passwords_data.json")

            pyperclip.copy(password_entry.get())
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


def update_websites_list(new_data, file_name):
    try:
        # Get old data
        with open(file_name, "r") as data_file:
            # Read the old data
            data = json.load(data_file)
    # If the file does not exist, then dump the new data directly
    except FileNotFoundError:
        with open(file_name, "w") as data_file:
            json.dump(new_data, data_file)
    else:
        # Update the old data
        data.update(new_data)

        # Save new data
        with open(file_name, "w") as data_file:
            json.dump(data, data_file, indent=4)


# ---------------------------- UI SETUP ------------------------------- #
if __name__ == '__main__':
    # Create main screen
    master = Tk()
    master.title("Password Manager")
    master.config(padx=50, pady=50)
    # Create the Canvas
    canvas = Canvas(master, width=200, height=200)
    img = Image.open("logo.png")
    img = ImageTk.PhotoImage(img)
    canvas.create_image(100, 100, image=img)
    canvas.grid(row=0, column=1)

    # Create the labels
    website_label = ttk.Label(text="Website name:")
    website_label.grid(row=1, column=0)
    user_label = ttk.Label(text="Email / User name:")
    user_label.grid(row=2, column=0)
    password_label = ttk.Label(text="Password:")
    password_label.grid(row=3, column=0)

    # Entries
    website_entry = ttk.Entry(width=35)
    website_entry.grid(row=1, column=1)
    website_entry.focus()
    user_entry = ttk.Entry(width=58)
    user_entry.grid(row=2, column=1, columnspan=2)
    user_entry.insert(0, "amgedelshiekh@gmail.com")
    password_entry = ttk.Entry(width=35)
    password_entry.grid(row=3, column=1)

    # Buttons
    # master.bind('<Return>', generate_password)
    generate_button = ttk.Button(
        text="Generate Password", width=21, command=generate_password)
    generate_button.grid(row=3, column=2)

    search_button = ttk.Button(
        text="Search", width=21, command=search_passwords)
    search_button.grid(row=1, column=2)

    add_button = ttk.Button(text="Add", width=58, command=save_data)
    add_button.grid(row=4, column=1, columnspan=2)

    master.mainloop()
