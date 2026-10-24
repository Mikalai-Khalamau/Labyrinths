import math
from typing import Any, ClassVar

from CellType import CellType
from Maze import Maze
from Path import Path

INFINITY = math.inf


class Solver:
    """Реализует алгоритмы нахождения пути в лабиринте - Дейкстра и А* (A-star)."""

    TWO_COORDS_LENGTH = 2
    DIRECTIONS_WITHOUT_BORDERS: ClassVar[list[tuple[int, int]]] = [
        (1, 0),
        (-1, 0),
        (0, -1),
        (0, 1),
    ]

    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int) -> None:
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def dijkstra_solve(self, maze: Maze) -> Maze:
        """Решение алгоритмом Дейкстра."""
        start_x = self.start_x
        start_y = self.start_y
        end_x = self.end_x
        end_y = self.end_y

        path = Path()
        height = maze.height
        width = maze.width
        distances = [[INFINITY for y in range(height)] for x in range(width)]
        distances[start_x][start_y] = 0
        visited_cells = set()
        parent_cell: dict[Any, Any] = {}

        while True:
            cell = None
            # Находим точку с минимальным расстоянием от стартовой
            min_distance = INFINITY
            for i in range(width):
                for j in range(height):
                    if (
                        (i, j) not in visited_cells
                        and maze.get_cell(i, j) == CellType.PASSABLE
                    ) and distances[i][j] < min_distance:
                        min_distance = distances[i][j]
                        cell = (i, j)

            if cell is None or min_distance == INFINITY:
                break
            x, y = cell
            visited_cells.add((x, y))
            if (x, y) == (end_x, end_y):  # достигнем конца и выйдем и прервем цикл
                break

            # Работаем со всеми соседями точки и если расстояние через нынешнюю точку
            # ближе, то обновляем
            for step_x, step_y in self.DIRECTIONS_WITHOUT_BORDERS:
                new_x, new_y = x + step_x, y + step_y
                if (
                    0 <= new_x < width
                    and 0 <= new_y < height
                    and maze.get_cell(new_x, new_y) == CellType.PASSABLE
                    and distances[x][y] + 1 < distances[new_x][new_y]
                ):
                    distances[new_x][new_y] = distances[x][y] + 1
                    parent_cell[(new_x, new_y)] = (x, y)

        # С конца восстанавливаем путь
        path.build_path(start_x, start_y, end_x, end_y, parent_cell)
        path.add_path_to_maze(maze)
        maze.set_cell(start_x, start_y, CellType.START)
        maze.set_cell(end_x, end_y, CellType.END)
        return maze

    def astar_solve(self, maze: Maze) -> Maze:
        """Решение алгоритмом A-Star."""
        start_x = self.start_x
        start_y = self.start_y
        end_x = self.end_x
        end_y = self.end_y

        # Манхеттенская эвристика для функции h
        # берем модули расстояний по осям в сумме
        def heuristic(x: int, y: int) -> int:
            return abs(x - end_x) + abs(y - end_y)

        path = Path()
        height = maze.height
        width = maze.width
        # g[x][y] - реальное расстояние от стартовой точки до точки (x,y).
        # Изначально у стартовой 0, у остальных - бесконечность. Проходя, обновляем.
        g = [[INFINITY for y in range(height)] for y in range(width)]
        # f[x][y] = g[x][y] + h[x][y].
        # С его помощью выбираем точку, в которую пойдем следующей.
        f = [[INFINITY for y in range(height)] for y in range(width)]
        g[start_x][start_y] = 0
        f[start_x][start_y] = heuristic(start_x, start_y)
        parent_cell = {}
        open_cells = [(start_x, start_y)]
        processed_cells = []

        while open_cells:
            min_distance = INFINITY
            cell = None
            # Находим ближайшую точку по эвристике и реальному расстоянию
            for s in open_cells:
                x, y = s
                if f[x][y] < min_distance:
                    min_distance = f[x][y]
                    cell = (x, y)
            (x, y) = cell
            if (x, y) == (end_x, end_y):
                break
            open_cells.remove((x, y))
            processed_cells.append((x, y))

            # Работаем с соседями точки и обновляемся
            # как в алгоритме Дейкстра, используя g
            for step_x, step_y in self.DIRECTIONS_WITHOUT_BORDERS:
                new_x, new_y = x + step_x, y + step_y
                if (
                    0 <= new_x < width
                    and 0 <= new_y < height
                    and maze.get_cell(new_x, new_y) == CellType.PASSABLE
                    and (new_x, new_y) not in processed_cells
                    and g[new_x][new_y] > g[x][y] + 1
                ):
                    g[new_x][new_y] = g[x][y] + 1
                    f[new_x][new_y] = heuristic(new_x, new_y) + g[new_x][new_y]
                    parent_cell[(new_x, new_y)] = (x, y)
                    open_cells.append((new_x, new_y))

        # Восстановление пути по словарю родителей
        message = "Путь до конечной точки не найден"
        if (end_x, end_y) not in parent_cell:
            raise KeyError(message)
        path.build_path(start_x, start_y, end_x, end_y, parent_cell)
        path.add_path_to_maze(maze)
        maze.set_cell(start_x, start_y, CellType.START)
        maze.set_cell(end_x, end_y, CellType.END)
        return maze
