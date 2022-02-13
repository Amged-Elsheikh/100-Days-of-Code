# --------------- Import libraries and set working directory ----------------- #
from tkinter import messagebox
from tkinter import *
import os
from PIL import Image, ImageTk
import pandas as pd
import random


BACKGROUND_COLOR = "#B1DDC6"

def show_messagebox():
    text = f"You have learnt all JLPT N{jlpt_lv} words"
    messagebox.showinfo(title="complete", message=text)


def show_jp_card():
    master.after_cancel(flip_timer)
    kanji, hiragana = df.loc[word_id, df.columns[0:2]]

    canvas.itemconfig(shown_card, image=front_image)
    canvas.itemconfig(title_text, text="Japanese")
    if type(kanji) == str:
        canvas.itemconfig(kanji_text, text=kanji)
        canvas.itemconfig(furi_text, text=hiragana)
    else:
        canvas.itemconfig(kanji_text, text=hiragana)
        canvas.itemconfig(furi_text, text="")


def get_front_card():
    global word_id, flip_timer
    if len(df) > 0:
        word_id = random.randint(0, df.index[-1])
        while word_id in learned_ids:
            word_id = random.randint(0, len(df)-1)
        show_jp_card()
        flip_timer = master.after(3000, func=get_translate)
    else:
        show_messagebox()


def get_translate():
    english_word = df.loc[word_id, df.columns[2]]
    canvas.itemconfig(shown_card, image=back_image)
    canvas.itemconfig(title_text, text="English")
    canvas.itemconfig(kanji_text, text=english_word)
    canvas.itemconfig(furi_text, text="")


def is_known():
    global df, learned_df
    if len(df)>0:
        learned_item = df.loc[word_id, df.columns]
        df.drop(word_id, inplace=True)
        learned_df = learned_df.append(learned_item)
        learned_ids.append(word_id)
        get_front_card()
    else:
        show_messagebox()


if __name__ == '__main__':
    jlpt_lv = 5

    DAY = "31"
    if DAY not in os.getcwd():
        sub_folder = list(filter(lambda x: DAY in x, os.listdir()))
        if sub_folder:
            os.chdir(os.path.join(os.getcwd(), sub_folder[0]))

    df = pd.read_csv(f"N{jlpt_lv} to learn.csv")
    learned_ids = []
    if os.path.exists(f"N{jlpt_lv} learned.csv"):
        learned_df = pd.read_csv(f"N{jlpt_lv} learned.csv")
    else:
        learned_df = pd.DataFrame(columns=df.columns)

    master = Tk()
    master.title("Flashy")
    master.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    front_image = PhotoImage(file=os.path.join("images", "card_front.png"))
    back_image = PhotoImage(file=os.path.join("images", "card_back.png"))

    canvas = Canvas(master, width=800, height=526,
                    bg=BACKGROUND_COLOR, highlightthickness=0)

    shown_card = canvas.create_image(
        400, 263, anchor=CENTER, image=front_image)
    title_text = canvas.create_text(
        400, 100, text="", font=("Aiel", 40, "italic"))
    furi_text = canvas.create_text(
        400, 230, text="", font=("Aiel", 30, "italic"))
    kanji_text = canvas.create_text(
        400, 320, text="", font=("Aiel", 35, "bold"), width=600)

    flip_timer = master.after(3000, get_translate)
    get_front_card()

    canvas.grid(row=0, column=0, columnspan=3)
    # canvas.create_text(x=400,y=150)

    right_button_image = PhotoImage(file=os.path.join("images", "right.png"))
    wrong_button_image = PhotoImage(file=os.path.join("images", "wrong.png"))
    jp_image = Image.open(os.path.join("images", "jp button.png"))
    jp_image = ImageTk.PhotoImage(jp_image.resize((100, 100), Image.ANTIALIAS))

    right_button = Button(image=right_button_image,
                          highlightthickness=0, command=is_known)
    wrong_button = Button(image=wrong_button_image,
                          highlightthickness=0, command=get_front_card)
    jp_button = Button(image=jp_image, highlightthickness=0,
                       command=show_jp_card)

    right_button.grid(row=1, column=2)
    wrong_button.grid(row=1, column=0)
    jp_button.grid(row=1, column=1)

    master.mainloop()

    df.to_csv(f"N{jlpt_lv} to learn.csv", index=False)
    learned_df.to_csv(f"N{jlpt_lv} learned.csv", index=False)
