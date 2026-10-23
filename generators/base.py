"""
Generator abstraction.

This is the extension point for new mental-math techniques.
"""

from abc import ABC, abstractmethod

from core.models import Question


class QuestionGenerator(ABC):

    @abstractmethod
    def generate(self) -> Question:
        """Generate one random question."""
        raise NotImplementedError
