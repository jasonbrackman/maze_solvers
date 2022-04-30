from collections import deque
from typing import Optional, Callable

from node import Node
from vec import Vec


def bfs(start: Vec, goal: Vec, neighbours: Callable) -> Optional[Node]:
    visited = {start, }
    q = deque([Node(start, parent=None)])
    while q:
        current = q.popleft()
        if current.pos == goal:
            return current

        for _, n in neighbours(current.pos):
            if n not in visited:
                visited.add(n)
                q.append(Node(n, parent=current))

    # Could not find a path.
    return None
