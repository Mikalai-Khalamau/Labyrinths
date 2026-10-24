import random
from random import choice
from typing import ClassVar

from CellType import CellType
from Maze import Maze


class Generator:
    """Создаем лабиринт алгоритмами Прима и DFS."""

    BIG_VALUE = 1000
    DIRECTIONS_WITH_BORDERS: ClassVar[list[tuple[int, int]]] = [
        (-2, 0),
        (2, 0),
        (0, -2),
        (0, 2),
    ]

    def __init__(self, width: int, height: int) -> None:
        self.check_sizes(width, height)
        self.width = width + 2
        self.height = height + 2

    def _is_correct_borders(self, check_x: int, check_y: int) -> bool:
        return 0 <= check_x < self.width and 0 <= check_y < self.height

    def prima_generate(self, *, is_unicode: bool = False) -> Maze:
        """Генерация методом Прима."""
        width = self.width
        height = self.height
        maze = Maze(width, height, is_unicode=is_unicode)
        # Начнем с нечетных координат - так лабиринт получается аккуратнее
        start_x = random.randrange(1, width - 1, 2)
        start_y = random.randrange(1, height - 1, 2)
        visited_cells = set()
        walls = []

        # Добавляем соседей и стены, через которые ходим
        def add_cell(x: int, y: int) -> None:
            maze.set_cell(x, y, CellType.PASSABLE)
            visited_cells.add((x, y))
            for dir_x, dir_y in self.DIRECTIONS_WITH_BORDERS:
                neighbour_x = x + dir_x
                neighbour_y = y + dir_y
                wall_x = x + dir_x // 2
                wall_y = y + dir_y // 2

                if (
                    self._is_correct_borders(neighbour_x, neighbour_y)
                    and maze.get_cell(neighbour_x, neighbour_y) == CellType.WALL
                ):
                    walls.append((wall_x, wall_y, neighbour_x, neighbour_y))

        # Начинаем алгоритм со стартовой ячейки
        # Рекурсивно пробиваем стены к соседям, начиная со стартовой точки
        add_cell(start_x, start_y)
        while walls:
            wall = choice(walls)
            wall_x, wall_y, point_x, point_y = wall
            walls.remove(wall)
            if (point_x, point_y) not in visited_cells:
                maze.set_cell(wall_x, wall_y, CellType.PASSABLE)
                add_cell(point_x, point_y)
        # Расставляем границы по периметру лабиринта и улучшаем четные лабиринты
        self._set_borders(maze)
        self._improve_even(maze)
        return maze

    def dfs_generate(self, *, is_unicode: bool = False) -> Maze:
        """Генерация методом DFS."""
        width = self.width
        height = self.height
        maze = Maze(width, height, is_unicode=is_unicode)
        # Начнем с нечетных координат - так лабиринт получается аккуратнее
        start_x = random.randrange(1, width - 1, 2)
        start_y = random.randrange(1, height - 1, 2)
        maze.set_cell(start_x, start_y, CellType.PASSABLE)
        stack = [(start_x, start_y)]  # Стек для прохода по вершинам
        visited_cells = set(stack)

        def step(x: int, y: int, i: int, j: int) -> bool:
            """Пробуем пробить стену. Добавляем в стек и посещенные."""
            if (
                self._is_correct_borders(x + i, y + j)
                and (x + i, y + j) not in visited_cells
            ):
                maze.set_cell(x + i // 2, y + j // 2, CellType.PASSABLE)
                maze.set_cell(x + i, y + j, CellType.PASSABLE)
                stack.append((x + i, y + j))
                visited_cells.add((x + i, y + j))
                return True
            return False

        def step_for_some_direction(x: int, y: int) -> None:
            """Когда пробьем хоть одну стену, то идем к следующей точке.

            Пробуем рандомно направления по очереди.
            """
            random.shuffle(self.DIRECTIONS_WITH_BORDERS)
            for dir_x, dir_y in self.DIRECTIONS_WITH_BORDERS:
                if step(x, y, dir_x, dir_y):
                    return
            stack.pop()

        while stack:
            x, y = stack[-1]
            step_for_some_direction(x, y)

        self._set_borders(maze)
        self._improve_even(maze)
        return maze

    def check_sizes(self, x: int, y: int) -> None:
        """Проверка положительности размеров лабиринта."""
        if x <= 0 or y <= 0:
            message = "Размеры должны быть положительными"
            raise ValueError(message)
        if x >= self.BIG_VALUE and y >= self.BIG_VALUE:
            message = "Размеры слишком велики"
            raise ValueError(message)

    def _improve_even(self, maze: Maze) -> None:
        """Метод, убирающий лишние стены в четных лабиринтах.

        Убираем через одну стенки в предпоследнем ряду
        и столбце снизу и справа в четных лабиринтах
        """
        if maze.width % 2 == 0 and maze.height % 2 == 0:
            for i in range(1, maze.height - 2):
                if (
                    maze.get_cell(maze.width - 2, i - 1) == CellType.WALL
                    and maze.get_cell(maze.width - 2, i + 1) == CellType.WALL
                ):
                    maze.set_cell(maze.width - 2, i, CellType.PASSABLE)
            for j in range(1, maze.width - 2):
                if (
                    maze.get_cell(j - 1, maze.height - 2) == CellType.WALL
                    and maze.get_cell(j + 1, maze.height - 2) == CellType.WALL
                ):
                    maze.set_cell(j, maze.height - 2, CellType.PASSABLE)

    def _set_borders(self, maze: Maze) -> None:
        """Расстановка стен по периметру. Получается лабиринт без выходов."""
        width = maze.width
        height = maze.height
        for i in range(width):
            maze.set_cell(i, 0, CellType.WALL)
            maze.set_cell(i, height - 1, CellType.WALL)
        for i in range(height):
            maze.set_cell(0, i, CellType.WALL)
            maze.set_cell(width - 1, i, CellType.WALL)
