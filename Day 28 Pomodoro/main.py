# --------------- Import libraries and set working directory ----------------- #
from tkinter import *
import os
from tkinter import ttk
from PIL import Image, ImageTk

if "28" not in os.getcwd():
    sub_folder = list(filter(lambda x: "28" in x, os.listdir()))
    if sub_folder:
        os.chdir(os.path.join(os.getcwd(), sub_folder[0]))

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 10
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 1
TIMER = None
# ---------------------------- TIMER RESET ----------------------------- #


def reset_timer():
    global reps, check_marks, TIMER
    master.after_cancel(TIMER)
    my_label.config(text="TIMER", fg=GREEN)
    canvas.itemconfig(canvas_timer, text="00:00")
    reps = 1
    check_marks = ""
    check_mark_label.config(text="")
# ---------------------------- TIMER MECHANISM ------------------------- #


def start_timer():
    global reps, check_marks
    if reps % 2 == 0:
        check_marks += "✓"
        check_mark_label.config(text=check_marks)

    if reps % 2 != 0:
        my_label.config(text="Work", fg=GREEN)
        count_down(WORK_MIN * 60)
        reps += 1
    elif reps == 8:
        my_label.config(text="Break", fg=RED)
        count_down(LONG_BREAK_MIN*60)
        reps = 1
    else:
        my_label.config(text="Break", fg=PINK)
        count_down(SHORT_BREAK_MIN*60)
        reps += 1
# ---------------------------- COUNTDOWN MECHANISM -------------------- #


def count_2_timer(count):
    minutes = str(count//60)
    seconds = str(count % 60)
    if len(minutes) == 1:
        minutes = f"0{minutes}"
    if len(seconds) == 1:
        seconds = f"0{seconds}"
    return minutes, seconds


def count_down(count):
    global TIMER
    minutes, seconds = count_2_timer(count)
    canvas.itemconfig(canvas_timer, text=f"{minutes}:{seconds}")
    if count >= 0:
        TIMER = master.after(1000, count_down, count-1)
    else:
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
if __name__ == '__main__':
    master = Tk()
    master.title("Pomodoro")
    master.config(padx=100, pady=50, bg=YELLOW)

    # Create canvas
    canvas = Canvas(master, width=200, height=224,
                    bg=YELLOW, highlightthickness=0)
    # Load the image
    img = Image.open("tomato.png")
    img = ImageTk.PhotoImage(img)
    # Add image to the canvas
    canvas.create_image(100, 112, anchor=CENTER, image=img)
    canvas_timer = canvas.create_text(
        100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

    canvas.grid(row=1, column=1)

    # Create the labels
    my_label = Label(master, text="TIMER", font=(
        FONT_NAME, 35, "bold"), fg=GREEN, bg=YELLOW)
    my_label.grid(row=0, column=1)

    check_marks = ""
    check_mark_label = Label(master,
                             bg=YELLOW, font=(FONT_NAME, 20, "bold"), fg=GREEN)
    check_mark_label.grid(row=3, column=1)

    # Create buttons
    start_button = ttk.Button(master, text="Start", command=start_timer)
    reset_button = ttk.Button(master, text="Reset", command=reset_timer)

    start_button.grid(row=2, column=0)
    reset_button.grid(row=2, column=2)

    master.mainloop()
