from typing import Dict, List

from core.models import Question
from distribution.distributor import SelectionAllocation
from topics.registry import TopicRegistry
from topics.tree import TopicNode


class ConsoleCLI:
    """Handles all interactive terminal input/output."""

    def __init__(self, registry: TopicRegistry) -> None:
        self.registry = registry

    def show_welcome(self) -> None:
        print("\n" + "-" * 72)
        print("Mental Math Practitioner")
        print("-" * 72)
        print()

    def select_topics(self) -> List[TopicNode]:
        print("Available topics:")
        self.registry.display_topics()
        print()
        print("Enter one or more topic IDs separated by spaces.")
        print("Examples: A      A.1 A.2      A S M.1")
        print()

        while True:
            raw = input("Select topics: ").strip()
            if not raw:
                print("Please select at least one topic.")
                continue

            ids = raw.split()
            try:
                nodes = self.registry.get_nodes(ids)
            except KeyError as exc:
                print(f"Unknown topic ID: {exc.args[0]}. Please try again.")
                continue

            return nodes

    def ask_question_count(self) -> int:
        while True:
            raw = input("Total number of questions: ").strip()
            try:
                count = int(raw)
            except ValueError:
                print("Please enter a positive integer.")
                continue

            if count <= 0:
                print("Question count must be greater than zero.")
                continue

            return count

    def show_distribution(self, allocation: Dict[str, SelectionAllocation]) -> None:
        print("\nQuestion distribution:")
        print("-" * 72)

        total = sum(item.question_count for item in allocation.values())

        for item in allocation.values():
            print(f"{item.path:<55} {item.question_count:>4} ({item.weight * 100:>6.2f}%)")

        print("-" * 72)
        print(f"{'Total':<55} {total:>4}")

    def wait_for_start(self) -> None:
        input("\nPress Enter to start the test...")

    def ask_answer(self, question: Question) -> str:
        return input(f"\n{question.text}\nYour answer: ").strip()

    def show_result(self, correct: bool, correct_answer: int) -> None:
        if correct:
            print("Correct!")
        else:
            print(f"Incorrect. Correct answer: {correct_answer}")
