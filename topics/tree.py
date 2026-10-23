from typing import List, Optional

from generators.base import QuestionGenerator


class TopicNode:
    """Represents one node in the mental-math topic hierarchy."""

    def __init__(self, name: str, node_id: str, generator: Optional[QuestionGenerator] = None) -> None:
        self.name = name
        self.node_id = node_id
        self.generator = generator
        self.parent: Optional["TopicNode"] = None
        self.children: List["TopicNode"] = []

    def add_child(self, child: "TopicNode") -> "TopicNode":
        """Attach a child and return it for convenient construction."""
        child.parent = self
        self.children.append(child)
        return child

    def is_leaf(self) -> bool:
        return not self.children

    def is_generatable(self) -> bool:
        """A node is directly selectable for generation when it has a generator."""
        return self.generator is not None

    def get_all_leaves(self) -> List["TopicNode"]:
        """Return every generatable descendant."""
        if self.is_generatable():
            return [self]

        leaves: List[TopicNode] = []
        for child in self.children:
            leaves.extend(child.get_all_leaves())
        return leaves

    def get_path(self) -> str:
        """Return a human-readable hierarchy path."""
        nodes = []
        current: Optional[TopicNode] = self

        while current is not None:
            nodes.append(current.name)
            current = current.parent

        return " > ".join(reversed(nodes))

    def display(self, indent: int = 0) -> None:
        """Print this subtree in a readable CLI format."""
        marker = "*" if self.is_generatable() else "+"
        print(f"{'  ' * indent}{self.node_id:<5} {marker} {self.name}")

        for child in self.children:
            child.display(indent + 1)
