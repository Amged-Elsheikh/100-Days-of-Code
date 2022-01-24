import tkinter as tk
from tkinter import ttk


def move_slider():
    miles_scale.set(float(miles_entry.get()))


def convert_distance():
    dist = float(miles_entry.get())
    km_output.config(text=round(dist*1.609, 3))


def update_miles():
    miles_entry.delete(0, "end")
    miles_entry.insert(tk.END, float(round(miles_scale.get(), 3)))


def move_km_slider():
    km_scale.set(float(miles_scale.get())*1.609)


def set_sliders(*args):
    miles = float(miles_entry.get())
    miles_scale.set(miles)
    pass


def all_slide_func(*args):
    update_miles()
    move_km_slider()
    convert_distance()


def update_km():
    km_output.config(text=round(float(km_scale.get()), 3))


def km_slide_func(*args):
    update_km()


# Main window
master = tk.Tk()
# Create a simple label text
my_label = ttk.Label(master, text="is equal to").grid(row=1, column=0)
# Create the Output label
km_output = ttk.Label(master, text="0.0")
km_output.grid(row=1, column=1)
km_label = ttk.Label(master, text="Km").grid(row=1, column=2)


miles_label = ttk.Label(master, text="Miles").grid(row=0, column=2)
miles_entry = ttk.Entry(master, width=10)
miles_entry.insert(tk.END, "0")
miles_entry.bind('<Return>', set_sliders)
miles_entry.grid(row=0, column=1)


km_scale = ttk.Scale(master, from_=0, to=100*1.609,
                     orient=tk.HORIZONTAL, command=km_slide_func)

miles_scale = ttk.Scale(master, from_=0, to=100,
                        orient=tk.HORIZONTAL, command=all_slide_func)

# miles_scale.config(command=all_slide_func)
miles_scale.set(0)

miles_scale.grid(row=0, column=3)
km_scale.grid(row=1, column=3)


master.mainloop()
