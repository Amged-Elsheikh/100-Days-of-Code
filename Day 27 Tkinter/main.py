# from tkinter import *
# from tkinter import ttk
# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# root.mainloop()


import tkinter as tk

master = tk.Tk()
master.title("1st GUI")
master.minsize(width=500, height=300)

my_label = tk.Label(master, text=f"First label", font=("Arial", 14))
# my_label.place(x=0,y=0)
my_label.config(padx=30, pady=10)
my_label.grid(row=0, column=0)


entry = tk.Entry(width=10)
entry.grid(row=2,column=3)

def button_click():
    new_text = entry.get()
    my_label.config(text=new_text)


button_1 = tk.Button(text="Excute", command=button_click)
button_1.grid(row=1, column=1)

button_2 = tk.Button(text="Do nothing")
button_2.grid(row=0, column=2)

master.mainloop()