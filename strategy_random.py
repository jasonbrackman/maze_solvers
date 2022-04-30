from random import choice
from typing import Optional, Callable

from node import Node
from vec import Vec


def random(start: Vec, goal: Vec, neighbours: Callable) -> Optional[Node]:
    node = Node(start, parent=None)
    while True:
        w, r = choice(list(neighbours(node.pos)))
        node = Node(pos=r, parent=node)
        if node.pos == goal:
            return node
