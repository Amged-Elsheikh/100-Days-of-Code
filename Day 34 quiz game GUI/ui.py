from tkinter import *
import os
from PIL import ImageTk, Image
from question_model import Exam

THEME_COLOR = "#375362"


class QuizInterface:
    def __init__(self) -> None:
        self.exam = Exam()

        self.master = Tk()
        self.master.config(bg=THEME_COLOR, padx=20, pady=20)
        self.master.title("Quizzer")

        self.score_label = Label(self.master,
                                 text=f"score: 0",
                                 bg=THEME_COLOR, fg="white",
                                 font=("Aiel", 20, "italic"))
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(self.master, height=250,
                             width=300, highlightthickness=0)
        self.question = self.canvas.create_text(
            150, 125, text=self.exam.show_question(),
            width=290, fill=THEME_COLOR,
            font=("Aiel", 20, "italic"))

        self.canvas.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

        true_image = Image.open(os.path.join("images", "true.png"))
        true_image = ImageTk.PhotoImage(true_image)
        false_image = Image.open(os.path.join("images", "false.png"))
        false_image = ImageTk.PhotoImage(false_image)

        self.true_button = Button(self.master,
                                  image=true_image,
                                  background=THEME_COLOR,
                                  command=self.is_True)
        self.false_button = Button(self.master,
                                   image=false_image,
                                   background=THEME_COLOR,
                                   command=self.is_False)

        self.true_button.grid(row=2, column=0, padx=20, pady=20)
        self.false_button.grid(row=2, column=1, padx=20, pady=20)

        self.master.mainloop()

    def is_True(self):
        self.give_feedback("true")

    def is_False(self):
        self.give_feedback("false")

    def get_next_question(self):
        self.canvas.configure(bg="white")
        if self.exam.question_number < len(self.exam.questions):
            q_text = self.exam.show_question()
            self.canvas.itemconfig(self.question, text=q_text)
        else:
            self.canvas.itemconfig(
                self.question, text="You have checked all the questions")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def give_feedback(self, answer: str):
        is_right = self.exam.is_correct_answer(answer)
        self.score_label.config(text=f"score: {self.exam.user_score}")
        if is_right:
            self.canvas.configure(bg="green")
        else:
            self.canvas.configure(bg="red")
        self.master.after(10, self.get_next_question)
        self.exam.question_number += 1


if __name__ == '__main__':
    DAY = "34"
    if DAY not in os.getcwd():
        sub_folder = list(filter(lambda x: DAY in x, os.listdir()))
        if sub_folder:
            os.chdir(os.path.join(os.getcwd(), sub_folder[0]))
    QuizInterface()
