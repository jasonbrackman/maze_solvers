from collections import defaultdict
from queue import PriorityQueue
from typing import Callable, Dict, List, Tuple, Set

from node import Node
from vec import Vec


def dijkstra(start: Vec, goal: Vec, neighbours: Callable) -> Node:
    paths = dict()
    paths[start] = None
    visited: Set[Vec] = set()

    # edges is the DB of cost between two vectors.  Default is -1 (a possible future move)
    # the edge cost between vectors will shift as the edge cost is discovered.
    edges: Dict[Vec, Dict[Vec, int]] = dict()

    # distances is the db of cost from start to the vector.  The start vector starts at
    # zero and the edge costs will accumulate.  All paths are taken in to consideration.
    # If two paths lead to the same spot and there is a cheaper route, the cheaper route
    # score is provided.
    distances = defaultdict(lambda: float('inf'))
    distances[start] = 0

    pq = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        visited.add(current_vertex)

        neighbours_: List[Tuple[int, Vec]] = list(neighbours(current_vertex))
        for weight, neighbour in neighbours_:
            if current_vertex not in edges:
                edges[current_vertex] = defaultdict(lambda: -1)
            edges[current_vertex][neighbour] = weight
            if neighbour not in paths:
                paths[neighbour] = current_vertex
                if edges[current_vertex][neighbour] != -1:  # we are skipping walls anyway...
                    if neighbour not in visited:
                        distance = edges[current_vertex][neighbour]
                        old_cost = distances[neighbour]
                        new_cost = distances[current_vertex] + distance
                        if new_cost < old_cost:
                            pq.put((new_cost, neighbour))
                            distances[neighbour] = new_cost
                            paths[neighbour] = current_vertex

    node = Node(goal, None)
    while paths[node.pos] is not None:
        g = paths[node.pos]
        node = Node(g, parent=node)
    return node
