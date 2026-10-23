from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Question:
    """One generated mental-math question."""

    text: str
    answer: int
    topic_id: str
    topic_path: str


@dataclass(frozen=True)
class QuestionResult:
    """Outcome and timing information for one attempted question."""

    question: Question
    user_answer: Optional[int]
    is_correct: bool
    elapsed_seconds: float


@dataclass(frozen=True)
class TestResult:
    """Complete result of one practice session."""

    question_results: Tuple[QuestionResult, ...]

    @property
    def total_questions(self) -> int:
        return len(self.question_results)

    @property
    def correct_count(self) -> int:
        return sum(r.is_correct for r in self.question_results)

    @property
    def incorrect_count(self) -> int:
        return self.total_questions - self.correct_count

    @property
    def accuracy(self) -> float:
        if self.total_questions == 0:
            return 0.0
        return self.correct_count / self.total_questions * 100.0

    @property
    def total_time(self) -> float:
        return sum(r.elapsed_seconds for r in self.question_results)

    @property
    def average_time(self) -> float:
        if not self.question_results:
            return 0.0
        return self.total_time / self.total_questions

    @property
    def min_time(self) -> float:
        if not self.question_results:
            return 0.0
        return min(r.elapsed_seconds for r in self.question_results)

    @property
    def max_time(self) -> float:
        if not self.question_results:
            return 0.0
        return max(r.elapsed_seconds for r in self.question_results)
