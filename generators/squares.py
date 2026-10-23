import random

from core.models import Question
from generators.base import QuestionGenerator


class TwoDigitSquareGenerator(QuestionGenerator):
    def generate(self) -> Question:
        n = random.randint(10, 99)
        return Question(f"{n}² = ?", n * n, "", "")


class ThreeDigitSquareGenerator(QuestionGenerator):
    def generate(self) -> Question:
        n = random.randint(100, 999)
        return Question(f"{n}² = ?", n * n, "", "")


class EndingFiveSquareGenerator(QuestionGenerator):
    def generate(self) -> Question:
        n = random.randint(1, 99) * 10 + 5
        return Question(f"{n}² = ?", n * n, "", "")
