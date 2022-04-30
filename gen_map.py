import random
from typing import List, Union

from PIL import Image, ImageFilter

from maze import Maze
from strategy_dijkstra import dijkstra


def gen_graph(rows: int, cols: int) -> List[List[Union[int, str]]]:
    graph = []

    random_sigma = random.randint(1000, 10000)
    blur_strength = random.random()

    img = Image.effect_noise((rows, cols), random_sigma)
    img = img.filter(ImageFilter.GaussianBlur(blur_strength))
    data = img.load()
    # img.show()
    for row in range(rows):
        graph.append([])
        for col in range(cols):
            graph[row].append(data[row, col] // 26)

    return graph


def main() -> None:
    rows = 18
    cols = 72
    graph = gen_graph(rows, cols)
    graph[0][0] = "S"
    graph[rows - 1][cols - 1] = "G"
    maze = Maze(graph)
    hm = maze.heat_map(maze.solve(dijkstra), title="Dijkstra")

    for x in hm:
        print(x)


if __name__ == "__main__":
    main()
