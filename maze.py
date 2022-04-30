from __future__ import annotations

import time
from typing import Iterator, Optional, Callable

import colorama
from colorama import Fore, Back

from node import Node
from vec import Vec


def time_it(func):
    def timed(self, *args, **kwargs):
        ts = time.process_time()
        result = func(self, *args, **kwargs)
        te = time.process_time()
        self._time = te - ts
        return result

    return timed


class Maze:
    def __init__(self, graph):
        self._graph = graph
        self._start: Vec = self.find_vec_for_value('S')
        self._goal: Vec = self.find_vec_for_value('G')

        self._time = float('inf')

    def find_vec_for_value(self, value: str) -> Vec:
        for row in range(len(self._graph)):
            for col in range(len(self._graph[row])):
                if self._graph[row][col] == value:
                    return Vec(row, col)
        raise ValueError(f"Maze does not contain an expected value: {value}")

    def neighbours(self, pos: Vec) -> Iterator[Vec]:
        for i in (1, -1):
            # row
            new_row = pos.row + i
            if -1 < new_row < len(self._graph):
                new = Vec(new_row, pos.col)
                cell = self._graph[new.row][new.col]
                if cell != '#':
                    weight = 1
                    if cell not in ('S', 'G'):
                        weight = int(cell)
                    yield weight, new

            # col
            new_col = pos.col + i
            if -1 < new_col < len(self._graph[0]):
                new = Vec(pos.row, new_col)
                cell = self._graph[new.row][new.col]
                weight = 1
                if cell != '#':
                    if cell not in ('S', 'G'):
                        weight = int(cell)
                    yield weight, new

    @time_it
    def solve(self, strategy: Callable) -> Optional[Node]:
        return strategy(self._start, self._goal, self.neighbours)

    @staticmethod
    def get_route_from_node(node: Node):
        marks = []
        while node.parent:
            marks.append(node.pos)
            node = node.parent
        return marks

    # __ display
    def heat_map(self, node, title=None):
        marks = self.get_route_from_node(node)
        colorama.init(autoreset=True)

        lines = []

        if title:
            lines.append(self.format_title(marks, title))

        for row in range(len(self._graph)):
            line = []
            for col in range(len(self._graph[0])):
                item: str = str(self._graph[row][col])

                if item == 'S':
                    line.append(Fore.GREEN + item + Fore.RESET)
                elif item == 'G':
                    line.append(Fore.RED + item + Fore.RESET)
                elif item == '#':
                    line.append(Fore.WHITE + item + Fore.RESET)
                elif Vec(row, col) in marks:
                    line.append(Back.BLACK + item + Back.RESET)
                else:
                    line.append(Fore.WHITE + item + Fore.RESET)

            lines.append(' '.join(line) + Fore.RESET)
        return lines

    def pprint(self, node, title=None):
        marks = self.get_route_from_node(node)
        colorama.init(autoreset=True)

        lines = []

        if title:
            lines.append(self.format_title(marks, title))

        for row in range(len(self._graph)):
            line = []
            for col in range(len(self._graph[0])):
                item: str = self._graph[row][col]
                if item == 'S':
                    line.append(Fore.GREEN + item)
                elif item == 'G':
                    line.append(Fore.RED + item)
                elif item == '#':
                    line.append(Fore.WHITE + item)
                elif Vec(row, col) in marks:
                    line.append(Fore.YELLOW + '*')
                else:
                    line.append(' ')

            lines.append(' '.join(line) + Fore.RESET)

        return lines

    def _get_sum_of_marks(self, marks) -> int:
        total = 0
        for vec in marks:
            val: str = self._graph[vec.row][vec.col]
            if isinstance(val, int) or val.isdigit():
                total += int(val)
        return total

    def format_title(self, marks, title) -> str:

        last_line = f'[{title} - {self._time:0.4f}s - {self._get_sum_of_marks(marks)}]'
        start = len(last_line)
        end = len(self._graph[0]) * 2 - 1
        last_line += ' ' * (end - start)
        return last_line
