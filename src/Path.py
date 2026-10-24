# Набор точек, ведущих к результату
from CellType import CellType
from Maze import Maze


class Path:
    """Класс пути от одной к другой точке, используется в алгоритмах решения."""

    def __init__(self) -> None:
        self.points = []

    def add_point(self, x: int, y: int) -> None:
        """Добавляет точку в путь."""
        self.points.append((x, y))

    def add_path_to_maze(self, maze: Maze) -> None:
        """Добавляет полный путь в лабиринт поточечно."""
        for point in self.points:
            x, y = point
            maze.set_cell(x, y, CellType.ROAD)

    def build_path(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        parent_cell: dict[tuple[int, int], tuple[int, int]],
    ) -> None:
        """Восстанавливаем путь по набору клеток с родителями."""
        x, y = end_x, end_y
        while (x, y) != (start_x, start_y):
            self.add_point(x, y)
            (x, y) = parent_cell[(x, y)]
        self.add_point(start_x, start_y)
