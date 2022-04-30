from __future__ import annotations

from typing import Optional

from vec import Vec


class Node:
    def __init__(self, pos: Vec, parent: Optional[Node] = None) -> None:
        self.pos = pos
        self.parent = parent