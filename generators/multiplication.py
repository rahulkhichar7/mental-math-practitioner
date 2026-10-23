import random

from core.models import Question
from generators.base import QuestionGenerator


class TwoByTwoMultiplicationGenerator(QuestionGenerator):
    def generate(self) -> Question:
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        return Question(f"{a} × {b} = ?", a * b, "", "")


class ThreeByOneMultiplicationGenerator(QuestionGenerator):
    def generate(self) -> Question:
        a = random.randint(100, 999)
        b = random.randint(2, 9)
        return Question(f"{a} × {b} = ?", a * b, "", "")


class TwoByTwoEndingFiveMultiplicationGenerator(QuestionGenerator):
    def generate(self) -> Question:
        # One operand is always a two-digit multiple of 10 plus 5.
        a = random.randint(1, 9) * 10 + 5
        b = random.randint(10, 99)
        return Question(f"{a} × {b} = ?", a * b, "", "")
