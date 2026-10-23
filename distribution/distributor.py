from dataclasses import dataclass
import random
from typing import Dict, List

from topics.tree import TopicNode


@dataclass(frozen=True)
class SelectionAllocation:
    """Allocation information for one generated leaf."""

    node_id: str
    path: str
    weight: float
    question_count: int


class QuestionDistributor:
    """Converts selected topic nodes into exact question counts."""

    def calculate_leaf_weights(self, selected_nodes: List[TopicNode]) -> Dict[str, float]:
        if not selected_nodes:
            raise ValueError("At least one topic must be selected.")

        weights: Dict[str, float] = {}
        initial_weight = 1.0 / len(selected_nodes)

        for node in selected_nodes:
            self._expand_selection(node, initial_weight, weights)

        total = sum(weights.values())
        if total <= 0:
            raise ValueError("Selection produced no generatable topics.")

        # Floating-point normalization protects against tiny accumulated error.
        return {node_id: weight / total for node_id, weight in weights.items()}

    def _expand_selection(
        self,
        node: TopicNode,
        incoming_weight: float,
        result: Dict[str, float],
    ) -> None:
        if node.is_generatable():
            result[node.node_id] = result.get(node.node_id, 0.0) + incoming_weight
            return

        children = node.children
        if not children:
            raise ValueError(f"Topic '{node.name}' has no descendants.")

        child_weight = incoming_weight / len(children)

        for child in children:
            self._expand_selection(child, child_weight, result)

    def allocate_question_counts(
        self,
        selected_nodes: List[TopicNode],
        total_questions: int,
    ) -> Dict[str, SelectionAllocation]:
        if total_questions <= 0:
            raise ValueError("Total questions must be positive.")

        weights = self.calculate_leaf_weights(selected_nodes)
        node_lookup = self._collect_nodes(selected_nodes)

        ideal_counts = {
            node_id: weight * total_questions
            for node_id, weight in weights.items()
        }
        counts = {node_id: int(value) for node_id, value in ideal_counts.items()}

        remaining = total_questions - sum(counts.values())

        # Largest remainder method gives an exact total while staying as close
        # as possible to the requested proportional weights.
        remainders = {
            node_id: ideal_counts[node_id] - counts[node_id]
            for node_id in ideal_counts
        }

        # Randomized tie breaking prevents the same topic from always winning
        # when two topics have exactly equal fractional remainders.
        grouped = list(remainders.items())
        random.shuffle(grouped)
        grouped.sort(key=lambda item: item[1], reverse=True)

        for node_id, _ in grouped[:remaining]:
            counts[node_id] += 1

        result: Dict[str, SelectionAllocation] = {}

        for node_id, weight in weights.items():
            node = node_lookup[node_id]
            result[node_id] = SelectionAllocation(
                node_id=node_id,
                path=node.get_path(),
                weight=weight,
                question_count=counts[node_id],
            )

        return result

    def _collect_nodes(
        self,
        selected_nodes: List[TopicNode],
    ) -> Dict[str, TopicNode]:
        lookup: Dict[str, TopicNode] = {}

        def visit(node: TopicNode) -> None:
            lookup[node.node_id] = node
            for child in node.children:
                visit(child)

        for node in selected_nodes:
            visit(node)

        return lookup
