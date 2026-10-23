import random

from core.models import Question
from generators.base import QuestionGenerator


class TwoDigitSubtractionGenerator(QuestionGenerator):
    def generate(self) -> Question:
        a, b = sorted(
            (random.randint(10, 99), random.randint(10, 99)),
            reverse=True,
        )
        return Question(f"{a} - {b} = ?", a - b, "", "")


class ThreeDigitSubtractionGenerator(QuestionGenerator):
    def generate(self) -> Question:
        a, b = sorted(
            (random.randint(100, 999), random.randint(100, 999)),
            reverse=True,
        )
        return Question(f"{a} - {b} = ?", a - b, "", "")


class FourDigitSubtractionGenerator(QuestionGenerator):
    def generate(self) -> Question:
        a, b = sorted(
            (random.randint(1000, 9999), random.randint(1000, 9999)),
            reverse=True,
        )
        return Question(f"{a} - {b} = ?", a - b, "", "")
