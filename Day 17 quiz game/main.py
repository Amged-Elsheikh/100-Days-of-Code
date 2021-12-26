from os import system
from random import shuffle
from data import question_data, logo


class Exam:
    def __init__(self, name: str) -> None:
        # data is a list of dictionaries with twi keys: "text" has the problem and "answer" either True or False
        self.name = name
        self.questions = question_data["results"]
        shuffle(self.questions)
        self.number_of_questions = int(input("How many questions do you want to take? "))
        
        if self.number_of_questions > len(self.questions):
            print(f"There are only {len(self.questions)} questions, {self.name} will take all of them")
            self.number_of_questions = len(self.questions)

        self.total_score = 0
        self.user_score = 0

    def show_question(self):
        """Show the question and ask user to anser it"""
        print(
            f'Q{self.total_score+1}: {self.questions[self.total_score]["question"]}')
        answer = input("Choose your answer [T] or [F]: ").lower()
        if answer == "t":
            answer = "True"
        elif answer == "f":
            answer = "False"
        else:
            answer = None
        return answer

    def is_correct_answer(self, answer):
        if answer == self.questions[self.total_score]["correct_answer"]:
            return True
        else:
            return False

    def take_exam(self):
        for _ in range(self.number_of_questions):
            answer = self.show_question()

            if self.is_correct_answer(answer):
                self.user_score += 1
                print("Correct answer ✅")
            else:
                if answer:
                    print("Wrong answer ❌.", end=" ")
                else:
                    print("Unknwon answer.", end=" ")
                print(
                    f"Correct answer is {self.questions[self.total_score]['correct_answer']}")
            self.total_score += 1
            if self.total_score < len(self.questions):
                print(
                    f"{self.name} current score is: {self.user_score}/{self.total_score}\n\n")
        self.get_result()

    def get_result(self):
        print(f"{self.name} final score is {self.user_score}/{self.total_score} ({round((self.user_score/self.total_score)*100, 2)}%)")


if __name__ == '__main__':
    system("cls")
    print(logo, end="\n\n")
    Ali = Exam("Ali")
    Ali.take_exam()
