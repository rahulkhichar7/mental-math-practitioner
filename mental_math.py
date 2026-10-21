"""
Mental Math Practice Engine
===========================
Single-file, extensible terminal application.

Run:
    python mental_math.py
"""

from __future__ import annotations

import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence


# ============================================================
# DOMAIN MODELS
# ============================================================

@dataclass
class Question:
    """One generated question and its expected answer."""
    text: str
    correct_answer: int
    topic_path: str
    generator_name: str


@dataclass
class QuestionResult:
    """Result of answering one question."""
    question: Question
    user_answer: int
    correct: bool
    time_taken: float


@dataclass
class TestResult:
    """Complete result of one practice session."""
    question_results: List[QuestionResult]

    @property
    def total_questions(self) -> int:
        return len(self.question_results)

    @property
    def correct(self) -> int:
        return sum(r.correct for r in self.question_results)

    @property
    def incorrect(self) -> int:
        return self.total_questions - self.correct

    @property
    def accuracy(self) -> float:
        if not self.total_questions:
            return 0.0
        return self.correct / self.total_questions * 100.0

    @property
    def total_time(self) -> float:
        return sum(r.time_taken for r in self.question_results)

    @property
    def average_time(self) -> float:
        if not self.question_results:
            return 0.0
        return self.total_time / self.total_questions

    @property
    def minimum_time(self) -> float:
        if not self.question_results:
            return 0.0
        return min(r.time_taken for r in self.question_results)

    @property
    def maximum_time(self) -> float:
        if not self.question_results:
            return 0.0
        return max(r.time_taken for r in self.question_results)


# ============================================================
# QUESTION GENERATOR ABSTRACTION
# ============================================================

class QuestionGenerator(ABC):
    """
    Strategy interface for generating questions.

    New question types should be implemented by creating a new
    subclass and implementing generate(). The rest of the
    application does not need to know how the question works.
    """

    @abstractmethod
    def generate(self) -> Question:
        """Generate one random question."""
        raise NotImplementedError

    def generator_name(self) -> str:
        """Return a readable generator name."""
        return self.__class__.__name__


# ============================================================
# ADDITION
# ============================================================

class TwoDigitAdditionGenerator(QuestionGenerator):
    """Generate two-digit + two-digit questions."""

    def generate(self) -> Question:
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        return Question(
            f"{a} + {b} = ?",
            a + b,
            "",
            self.generator_name(),
        )


class ThreeDigitAdditionGenerator(QuestionGenerator):
    """Generate three-digit + three-digit questions."""

    def generate(self) -> Question:
        a = random.randint(100, 999)
        b = random.randint(100, 999)
        return Question(
            f"{a} + {b} = ?",
            a + b,
            "",
            self.generator_name(),
        )


class FourDigitAdditionGenerator(QuestionGenerator):
    """Generate four-digit + four-digit questions."""

    def generate(self) -> Question:
        a = random.randint(1000, 9999)
        b = random.randint(1000, 9999)
        return Question(
            f"{a} + {b} = ?",
            a + b,
            "",
            self.generator_name(),
        )


# ============================================================
# SUBTRACTION
# ============================================================

class TwoDigitSubtractionGenerator(QuestionGenerator):
    """Generate non-negative two-digit subtraction questions."""

    def generate(self) -> Question:
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        a, b = max(a, b), min(a, b)
        return Question(
            f"{a} - {b} = ?",
            a - b,
            "",
            self.generator_name(),
        )


class ThreeDigitSubtractionGenerator(QuestionGenerator):
    """Generate non-negative three-digit subtraction questions."""

    def generate(self) -> Question:
        a = random.randint(100, 999)
        b = random.randint(100, 999)
        a, b = max(a, b), min(a, b)
        return Question(
            f"{a} - {b} = ?",
            a - b,
            "",
            self.generator_name(),
        )


class FourDigitSubtractionGenerator(QuestionGenerator):
    """Generate non-negative four-digit subtraction questions."""

    def generate(self) -> Question:
        a = random.randint(1000, 9999)
        b = random.randint(1000, 9999)
        a, b = max(a, b), min(a, b)
        return Question(
            f"{a} - {b} = ?",
            a - b,
            "",
            self.generator_name(),
        )


# ============================================================
# MULTIPLICATION
# ============================================================

class TwoByTwoMultiplicationGenerator(QuestionGenerator):
    """Generate two-digit × two-digit questions."""

    def generate(self) -> Question:
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        return Question(
            f"{a} × {b} = ?",
            a * b,
            "",
            self.generator_name(),
        )


class ThreeByOneMultiplicationGenerator(QuestionGenerator):
    """Generate three-digit × one-digit questions."""

    def generate(self) -> Question:
        a = random.randint(100, 999)
        b = random.randint(2, 9)
        return Question(
            f"{a} × {b} = ?",
            a * b,
            "",
            self.generator_name(),
        )


class TwoByTwoEndingFiveMultiplicationGenerator(QuestionGenerator):
    """Generate 2×2 multiplication where at least one number ends in 5."""

    def generate(self) -> Question:
        if random.choice([True, False]):
            a = random.choice(range(15, 100, 10))
            b = random.randint(10, 99)
        else:
            a = random.randint(10, 99)
            b = random.choice(range(15, 100, 10))

        return Question(
            f"{a} × {b} = ?",
            a * b,
            "",
            self.generator_name(),
        )


# ============================================================
# SQUARES
# ============================================================

class TwoDigitSquareGenerator(QuestionGenerator):
    """Generate squares of two-digit numbers."""

    def generate(self) -> Question:
        a = random.randint(10, 99)
        return Question(
            f"{a}² = ?",
            a * a,
            "",
            self.generator_name(),
        )


class ThreeDigitSquareGenerator(QuestionGenerator):
    """Generate squares of three-digit numbers."""

    def generate(self) -> Question:
        a = random.randint(100, 999)
        return Question(
            f"{a}² = ?",
            a * a,
            "",
            self.generator_name(),
        )


class EndingFiveSquareGenerator(QuestionGenerator):
    """Generate squares of numbers ending in 5."""

    def generate(self) -> Question:
        a = random.choice(range(15, 1000, 10))
        return Question(
            f"{a}² = ?",
            a * a,
            "",
            self.generator_name(),
        )


# ============================================================
# HIERARCHICAL TOPIC NODE
# ============================================================

class TopicNode:
    """
    Generic tree node representing a topic/subtopic.

    A node may have children and/or a QuestionGenerator.
    Usually generators are attached to leaf nodes.

    The hierarchy itself is independent of the arithmetic logic.
    """

    def __init__(
        self,
        name: str,
        node_id: str,
        generator: Optional[QuestionGenerator] = None,
    ):
        self.name = name
        self.node_id = node_id
        self.generator = generator
        self.parent: Optional["TopicNode"] = None
        self.children: List["TopicNode"] = []

    def add_child(self, child: "TopicNode") -> None:
        """Attach a child and establish the parent relationship."""
        child.parent = self
        self.children.append(child)

    def is_leaf(self) -> bool:
        """Return whether this node has no children."""
        return not self.children

    def is_generatable(self) -> bool:
        """Return whether this node owns a question generator."""
        return self.generator is not None

    def get_all_leaves(self) -> List["TopicNode"]:
        """Recursively collect all generatable leaves below this node."""
        if self.is_leaf():
            return [self] if self.is_generatable() else []

        leaves: List[TopicNode] = []
        for child in self.children:
            leaves.extend(child.get_all_leaves())
        return leaves

    def get_path(self) -> str:
        """Return the complete path from root to this node."""
        path = []
        current: Optional[TopicNode] = self
        while current is not None:
            path.append(current.name)
            current = current.parent
        return " > ".join(reversed(path))

    def display(self, level: int = 0) -> None:
        """Recursively display this node and all descendants."""
        indent = "    " * level
        marker = " [QUESTION TYPE]" if self.is_generatable() else ""
        print(f"{indent}{self.node_id} - {self.name}{marker}")
        for child in self.children:
            child.display(level + 1)


# ============================================================
# TOPIC REGISTRY
# ============================================================

class TopicRegistry:
    """
    Builds and stores the application's topic hierarchy.

    This is the configuration/composition root for the current
    mental-math content. The rest of the application is generic.
    """

    def __init__(self):
        self.roots: List[TopicNode] = []
        self._nodes_by_id: Dict[str, TopicNode] = {}
        self._build_topics()

    def _register_root(self, node: TopicNode) -> None:
        """Register a root node and all descendants."""
        self.roots.append(node)
        self._register_recursively(node)

    def _register_recursively(self, node: TopicNode) -> None:
        """Register one node and recursively register its children."""
        if node.node_id in self._nodes_by_id:
            raise ValueError(f"Duplicate node ID: {node.node_id}")

        self._nodes_by_id[node.node_id] = node

        for child in node.children:
            self._register_recursively(child)

    def get_node(self, node_id: str) -> Optional[TopicNode]:
        """Find a topic node by its unique ID."""
        return self._nodes_by_id.get(node_id)

    def display(self) -> None:
        """Display the complete topic hierarchy."""
        print("\n" + "=" * 70)
        print("AVAILABLE MENTAL MATH TOPICS")
        print("=" * 70)
        for root in self.roots:
            root.display()
        print("=" * 70)

    def _build_topics(self) -> None:
        """
        Build the initial hierarchy.

        To add a new topic:
          1. Create its QuestionGenerator subclass.
          2. Create TopicNode objects.
          3. Connect them with add_child().
          4. Register the root.

        No engine/session/reporting changes are required.
        """

        # Addition
        addition = TopicNode("Addition", "A")
        addition.add_child(TopicNode(
            "Two-digit addition", "A.1",
            TwoDigitAdditionGenerator()
        ))
        addition.add_child(TopicNode(
            "Three-digit addition", "A.2",
            ThreeDigitAdditionGenerator()
        ))
        addition.add_child(TopicNode(
            "Four-digit addition", "A.3",
            FourDigitAdditionGenerator()
        ))
        self._register_root(addition)

        # Subtraction
        subtraction = TopicNode("Subtraction", "S")
        subtraction.add_child(TopicNode(
            "Two-digit subtraction", "S.1",
            TwoDigitSubtractionGenerator()
        ))
        subtraction.add_child(TopicNode(
            "Three-digit subtraction", "S.2",
            ThreeDigitSubtractionGenerator()
        ))
        subtraction.add_child(TopicNode(
            "Four-digit subtraction", "S.3",
            FourDigitSubtractionGenerator()
        ))
        self._register_root(subtraction)

        # Multiplication
        multiplication = TopicNode("Multiplication", "M")
        multiplication.add_child(TopicNode(
            "Two × Two digit", "M.1",
            TwoByTwoMultiplicationGenerator()
        ))
        multiplication.add_child(TopicNode(
            "Three × One digit", "M.2",
            ThreeByOneMultiplicationGenerator()
        ))
        multiplication.add_child(TopicNode(
            "Two × Two digit, one number ends in 5", "M.3",
            TwoByTwoEndingFiveMultiplicationGenerator()
        ))
        self._register_root(multiplication)

        # Square
        square = TopicNode("Square", "Q")
        square.add_child(TopicNode(
            "Two-digit square", "Q.1",
            TwoDigitSquareGenerator()
        ))
        square.add_child(TopicNode(
            "Three-digit square", "Q.2",
            ThreeDigitSquareGenerator()
        ))
        square.add_child(TopicNode(
            "Number ending in 5", "Q.3",
            EndingFiveSquareGenerator()
        ))
        self._register_root(square)


# ============================================================
# QUESTION ALLOCATION
# ============================================================

@dataclass
class SelectionAllocation:
    """Final weight and integer question count for one leaf."""
    node: TopicNode
    weight: float
    question_count: int


class QuestionDistributor:
    """
    Implements recursive hierarchical weighting.

    If N nodes are manually selected, each gets 1/N of the test.

    An internal selected node then divides its weight equally
    among its children, recursively.

    Integer counts are produced using the largest-remainder method.
    """

    @staticmethod
    def _expand_selection(
        node: TopicNode,
        incoming_weight: float,
        result: Dict[TopicNode, float],
    ) -> None:
        """Recursively propagate a selected node's weight to leaves."""
        if node.is_leaf():
            if node.is_generatable():
                result[node] = (
                    result.get(node, 0.0) + incoming_weight
                )
            return

        child_weight = incoming_weight / len(node.children)

        for child in node.children:
            QuestionDistributor._expand_selection(
                child, child_weight, result
            )

    @staticmethod
    def calculate_leaf_weights(
        selected_nodes: Sequence[TopicNode],
    ) -> Dict[TopicNode, float]:
        """Calculate final normalized weights for all selected leaves."""
        if not selected_nodes:
            return {}

        top_weight = 1.0 / len(selected_nodes)
        weights: Dict[TopicNode, float] = {}

        for node in selected_nodes:
            QuestionDistributor._expand_selection(
                node, top_weight, weights
            )

        return weights

    @staticmethod
    def allocate_question_counts(
        selected_nodes: Sequence[TopicNode],
        total_questions: int,
    ) -> List[SelectionAllocation]:
        """
        Convert fractional leaf weights into integer question counts.

        Uses largest-remainder allocation so the total is exactly
        total_questions while staying as close as possible to the
        desired weights.
        """
        weights = QuestionDistributor.calculate_leaf_weights(
            selected_nodes
        )

        if not weights or total_questions <= 0:
            return []

        leaves = list(weights.keys())
        ideal = {
            leaf: weights[leaf] * total_questions
            for leaf in leaves
        }

        counts = {
            leaf: int(ideal[leaf])
            for leaf in leaves
        }

        remaining = total_questions - sum(counts.values())

        remainders = [
            (leaf, ideal[leaf] - counts[leaf])
            for leaf in leaves
        ]

        # Randomize equal-remainder ties to avoid persistent bias.
        random.shuffle(remainders)
        remainders.sort(
            key=lambda item: item[1],
            reverse=True
        )

        for i in range(remaining):
            counts[remainders[i][0]] += 1

        return [
            SelectionAllocation(
                node=leaf,
                weight=weights[leaf],
                question_count=counts[leaf],
            )
            for leaf in leaves
        ]


# ============================================================
# QUESTION FACTORY
# ============================================================

class QuestionFactory:
    """
    Converts allocations into actual questions.

    Distribution and question generation are deliberately separate.
    """

    @staticmethod
    def create_questions(
        allocations: Sequence[SelectionAllocation],
    ) -> List[Question]:
        """Generate the requested number of questions and shuffle them."""
        questions: List[Question] = []

        for allocation in allocations:
            generator = allocation.node.generator
            if generator is None:
                continue

            for _ in range(allocation.question_count):
                question = generator.generate()
                question.topic_path = allocation.node.get_path()
                questions.append(question)

        random.shuffle(questions)
        return questions


# ============================================================
# CLI
# ============================================================

class CLI:
    """Owns terminal input/output and nothing else."""

    @staticmethod
    def read_positive_integer(prompt: str) -> int:
        """Read a positive integer from the user."""
        while True:
            try:
                value = int(input(prompt).strip())
                if value > 0:
                    return value
            except ValueError:
                pass
            print("Please enter a positive integer.")

    @staticmethod
    def parse_selection(
        user_input: str,
        registry: TopicRegistry,
    ) -> List[TopicNode]:
        """Convert space-separated node IDs into TopicNode objects."""
        selected: List[TopicNode] = []
        seen = set()

        for token in user_input.split():
            node = registry.get_node(token)

            if node is None:
                print(f"Warning: '{token}' is not a valid topic ID.")
                continue

            if token not in seen:
                seen.add(token)
                selected.append(node)

        return selected

    @staticmethod
    def ask_for_selection(
        registry: TopicRegistry,
    ) -> List[TopicNode]:
        """Display hierarchy and read the user's selections."""
        registry.display()

        print("\nSelection examples:")
        print("  A              -> entire Addition topic")
        print("  A.1            -> only two-digit addition")
        print("  A S M.1        -> mix topics and subtopics")
        print()

        while True:
            selected = CLI.parse_selection(
                input("Select topics/subtopics: "),
                registry,
            )

            if selected:
                return selected

            print("No valid selection found. Try again.")

    @staticmethod
    def show_allocation(
        allocations: Sequence[SelectionAllocation],
        total_questions: int,
    ) -> None:
        """Show the final question distribution before the test."""
        print("\n" + "=" * 70)
        print("QUESTION DISTRIBUTION")
        print("=" * 70)
        print(f"Total questions: {total_questions}\n")

        for allocation in allocations:
            print(
                f"{allocation.node.get_path():55} | "
                f"{allocation.weight * 100:6.2f}% | "
                f"{allocation.question_count:3} questions"
            )

        print("=" * 70)

    @staticmethod
    def wait_for_start() -> None:
        """Wait until the user is ready."""
        input("\nPress Enter when you are ready to start...")


# ============================================================
# TEST SESSION
# ============================================================

class TestSession:
    """Runs the generated questions and records timing/results."""

    def __init__(self, questions: Sequence[Question]):
        self.questions = list(questions)

    def run(self) -> TestResult:
        """Run the interactive test."""
        results: List[QuestionResult] = []

        print("\n" + "=" * 70)
        print("MENTAL MATH TEST")
        print("=" * 70)
        print(f"Questions: {len(self.questions)}")
        print("Enter only the numerical answer.")
        print("=" * 70)

        for index, question in enumerate(
            self.questions, start=1
        ):
            print(f"\n[{index}/{len(self.questions)}] {question.text}")

            start = time.perf_counter()

            while True:
                try:
                    answer = int(input("Answer: ").strip())
                    break
                except ValueError:
                    print("Please enter an integer.")

            elapsed = time.perf_counter() - start
            correct = answer == question.correct_answer

            results.append(
                QuestionResult(
                    question=question,
                    user_answer=answer,
                    correct=correct,
                    time_taken=elapsed,
                )
            )

            if correct:
                print(f"Correct! [{elapsed:.2f} sec]")
            else:
                print(
                    f"Wrong. Correct answer: "
                    f"{question.correct_answer} "
                    f"[{elapsed:.2f} sec]"
                )

        return TestResult(results)


# ============================================================
# REPORTING
# ============================================================

class ReportGenerator:
    """
    Generates the terminal report.

    Kept separate from TestSession so future output formats
    (CSV, JSON, database, web dashboard, etc.) can be added
    without changing test execution.
    """

    @staticmethod
    def print_report(result: TestResult) -> None:
        """Print overall statistics and wrong answers."""
        print("\n\n" + "=" * 70)
        print("TEST REPORT")
        print("=" * 70)

        print(f"Total Questions : {result.total_questions}")
        print(f"Correct         : {result.correct}")
        print(f"Incorrect       : {result.incorrect}")
        print(f"Accuracy        : {result.accuracy:.2f}%")
        print()
        print(f"Total Time      : {result.total_time:.2f} sec")
        print(f"Average Time    : {result.average_time:.2f} sec")
        print(f"Minimum Time    : {result.minimum_time:.2f} sec")
        print(f"Maximum Time    : {result.maximum_time:.2f} sec")

        wrong = [
            r for r in result.question_results
            if not r.correct
        ]

        if wrong:
            print("\n" + "=" * 70)
            print("WRONG ANSWERS")
            print("=" * 70)

            for i, item in enumerate(wrong, start=1):
                print(f"\n{i}. {item.question.text}")
                print(f"   Your answer    : {item.user_answer}")
                print(
                    f"   Correct answer : "
                    f"{item.question.correct_answer}"
                )
                print(f"   Time           : {item.time_taken:.2f} sec")
                print(f"   Topic          : {item.question.topic_path}")
        else:
            print("\nExcellent! No wrong answers.")

        print("\n" + "=" * 70)


# ============================================================
# APPLICATION SERVICE
# ============================================================

class MentalMathApplication:
    """Coordinates the registry, distribution, generation and session."""

    def __init__(self, registry: TopicRegistry):
        self.registry = registry

    def run(self) -> None:
        """Run one complete practice session."""
        print("\n" + "=" * 70)
        print("             MENTAL MATH ENGINE")
        print("=" * 70)

        selected = CLI.ask_for_selection(self.registry)

        total = CLI.read_positive_integer(
            "\nNumber of questions: "
        )

        allocations = QuestionDistributor.allocate_question_counts(
            selected,
            total,
        )

        if not allocations:
            print("No generatable question types were selected.")
            return

        CLI.show_allocation(allocations, total)
        CLI.wait_for_start()

        questions = QuestionFactory.create_questions(
            allocations
        )

        result = TestSession(questions).run()
        ReportGenerator.print_report(result)


# ============================================================
# ENTRY POINT
# ============================================================

def main() -> None:
    """Application entry point."""
    registry = TopicRegistry()
    app = MentalMathApplication(registry)

    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nPractice session terminated.")


if __name__ == "__main__":
    main()
