from typing import Callable, Optional

from node import Node
from vec import Vec


def dfs(start: Vec, goal: Vec, neighbours: Callable) -> Optional[Node]:
    visited = {start, }
    q = [Node(start, parent=None)]
    while q:
        current = q.pop()
        if current.pos == goal:
            return current

        for _, n in neighbours(current.pos):
            if n not in visited:
                visited.add(n)
                q.append(Node(n, parent=current))

    # Could not find a path
    return None
