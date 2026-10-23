import time
from typing import List, Sequence

from cli.console import ConsoleCLI
from core.models import Question, QuestionResult, TestResult


class TestSession:
    """Runs an interactive timed test."""

    def run(self, questions: Sequence[Question]) -> TestResult:
        
        cli = ConsoleCLI.__new__(ConsoleCLI)

        results: List[QuestionResult] = []

        for index, question in enumerate(questions, start=1):
            print(f"\nQuestion {index}/{len(questions)}")

            start = time.perf_counter()
            raw_answer = cli.ask_answer(question)
            elapsed = time.perf_counter() - start

            user_answer = self._parse_answer(raw_answer)
            is_correct = user_answer == question.answer

            cli.show_result(is_correct, question.answer)

            results.append(
                QuestionResult(
                    question=question,
                    user_answer=user_answer,
                    is_correct=is_correct,
                    elapsed_seconds=elapsed,
                )
            )

        return TestResult(tuple(results))

    @staticmethod
    def _parse_answer(raw_answer: str):
        """Convert a terminal answer to int; invalid input becomes None."""
        try:
            return int(raw_answer)
        except (TypeError, ValueError):
            return None
