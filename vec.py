from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, order=True)
class Vec:
    row: int
    col: int

    def __add__(self, other):
        return Vec(self.row + other.row, self.col + other.col)
