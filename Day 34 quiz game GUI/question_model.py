from data import get_questions
import html


class Exam:
    def __init__(self) -> None:
        self.questions = get_questions()
        self.question_number = 0
        self.user_score = 0

    def show_question(self) -> str:
        """Show the question and ask user to answer it"""
        q_text = html.unescape(
            self.questions[self.question_number]["question"])
        q_text = f'Q{self.question_number+1}:' + q_text
        return q_text

    def is_correct_answer(self, answer: str) -> bool:
        if answer == self.questions[self.question_number]["correct_answer"].lower():
            self.user_score += 1
            return True
        else:
            return False


if __name__ == '__main__':
    Ali = Exam()
