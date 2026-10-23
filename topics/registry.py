"""
Topic composition root.

This is the one place where the concrete generators are connected to the
generic topic tree. The rest of the application depends only on abstractions.

Adding a new practice type:
    1. Implement a QuestionGenerator subclass.
    2. Instantiate it here.
    3. Attach its TopicNode to the desired parent.

The distributor, session, and report code do not need to change.
"""

import random
from typing import Dict, Iterable, List

from core.models import Question
from distribution.distributor import SelectionAllocation
from generators.addition import (
    FourDigitAdditionGenerator,
    ThreeDigitAdditionGenerator,
    TwoDigitAdditionGenerator,
)
from generators.multiplication import (
    ThreeByOneMultiplicationGenerator,
    TwoByTwoEndingFiveMultiplicationGenerator,
    TwoByTwoMultiplicationGenerator,
)
from generators.squares import (
    EndingFiveSquareGenerator,
    ThreeDigitSquareGenerator,
    TwoDigitSquareGenerator,
)
from generators.subtraction import (
    FourDigitSubtractionGenerator,
    ThreeDigitSubtractionGenerator,
    TwoDigitSubtractionGenerator,
)
from topics.tree import TopicNode


class TopicRegistry:
    """Owns the application's topic tree and generator connections."""

    def __init__(self) -> None:
        self.roots: List[TopicNode] = []
        self._nodes: Dict[str, TopicNode] = {}
        self._build_topics()

    def _register(self, node: TopicNode) -> TopicNode:
        if node.node_id in self._nodes:
            raise ValueError(f"Duplicate topic ID: {node.node_id}")

        self._nodes[node.node_id] = node
        return node

    def _add_root(self, node: TopicNode) -> TopicNode:
        self._register(node)
        self.roots.append(node)
        return node

    def _add_child(self, parent: TopicNode, node: TopicNode) -> TopicNode:
        parent.add_child(node)
        self._register(node)
        return node

    def _build_topics(self) -> None:
        # Addition
        addition = self._add_root(TopicNode("Addition", "A"))
        self._add_child(
            addition,
            TopicNode(
                "Two-digit addition",
                "A.1",
                TwoDigitAdditionGenerator(),
            ),
        )
        self._add_child(
            addition,
            TopicNode(
                "Three-digit addition",
                "A.2",
                ThreeDigitAdditionGenerator(),
            ),
        )
        self._add_child(
            addition,
            TopicNode(
                "Four-digit addition",
                "A.3",
                FourDigitAdditionGenerator(),
            ),
        )

        # Subtraction
        subtraction = self._add_root(TopicNode("Subtraction", "S"))
        self._add_child(
            subtraction,
            TopicNode(
                "Two-digit subtraction",
                "S.1",
                TwoDigitSubtractionGenerator(),
            ),
        )
        self._add_child(
            subtraction,
            TopicNode(
                "Three-digit subtraction",
                "S.2",
                ThreeDigitSubtractionGenerator(),
            ),
        )
        self._add_child(
            subtraction,
            TopicNode(
                "Four-digit subtraction",
                "S.3",
                FourDigitSubtractionGenerator(),
            ),
        )

        # Multiplication
        multiplication = self._add_root(TopicNode("Multiplication", "M"))
        self._add_child(
            multiplication,
            TopicNode(
                "Two × two digit",
                "M.1",
                TwoByTwoMultiplicationGenerator(),
            ),
        )
        self._add_child(
            multiplication,
            TopicNode(
                "Three × one digit",
                "M.2",
                ThreeByOneMultiplicationGenerator(),
            ),
        )
        self._add_child(
            multiplication,
            TopicNode(
                "Two × two digit, one number ends in 5",
                "M.3",
                TwoByTwoEndingFiveMultiplicationGenerator(),
            ),
        )

        # Squares
        squares = self._add_root(TopicNode("Squares", "Q"))
        self._add_child(
            squares,
            TopicNode(
                "Two-digit square",
                "Q.1",
                TwoDigitSquareGenerator(),
            ),
        )
        self._add_child(
            squares,
            TopicNode(
                "Three-digit square",
                "Q.2",
                ThreeDigitSquareGenerator(),
            ),
        )
        self._add_child(
            squares,
            TopicNode(
                "Number ending in 5",
                "Q.3",
                EndingFiveSquareGenerator(),
            ),
        )

    def get_node(self, node_id: str) -> TopicNode:
        return self._nodes[node_id]

    def get_nodes(self, node_ids: Iterable[str]) -> List[TopicNode]:
        ids = list(node_ids)
        if len(set(ids)) != len(ids):
            raise ValueError("A topic cannot be selected more than once.")

        return [self.get_node(node_id) for node_id in ids]

    def display_topics(self) -> None:
        for root in self.roots:
            root.display()

    def create_questions(self, allocation: Dict[str, SelectionAllocation]) -> List[Question]:
        """
        Generate exactly the allocated number of questions and shuffle them.
        The final order is intentionally independent of topic distribution.
        """
        questions: List[Question] = []

        for item in allocation.values():
            node = self._nodes[item.node_id]

            if node.generator is None:
                raise ValueError(
                    f"Node '{node.node_id}' cannot directly generate questions."
                )

            for _ in range(item.question_count):
                generated = node.generator.generate()
                questions.append(
                    Question(
                        text=generated.text,
                        answer=generated.answer,
                        topic_id=node.node_id,
                        topic_path=node.get_path(),
                    )
                )

        random.shuffle(questions)
        return questions
