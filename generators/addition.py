"""Addition question generators."""

import random

from core.models import Question
from generators.base import QuestionGenerator


class TwoDigitAdditionGenerator(QuestionGenerator):
    def generate(self) -> Question:
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        return Question(f"{a} + {b} = ?", a + b, "", "")


class ThreeDigitAdditionGenerator(QuestionGenerator):
    def generate(self) -> Question:
        a = random.randint(100, 999)
        b = random.randint(100, 999)
        return Question(f"{a} + {b} = ?", a + b, "", "")


class FourDigitAdditionGenerator(QuestionGenerator):
    def generate(self) -> Question:
        a = random.randint(1000, 9999)
        b = random.randint(1000, 9999)
        return Question(f"{a} + {b} = ?", a + b, "", "")
