from pathlib import Path

from CellType import ASCII_TO_UNICODE, UNICODE_TO_ASCII, CellType


class Maze:
    """Класс лабиринта и методы ввода/вывода."""

    def __init__(self, width: int, height: int, *, is_unicode: bool = False) -> None:
        self.width = width
        self.height = height
        self.is_unicode = is_unicode
        # Изначально генерируем поле только из стен, а затем с помощью алгоритмов
        # удаляем стены и прокладываем дороги
        self._cells = [[CellType.WALL for _ in range(height)] for _ in range(width)]

    def set_cell(self, x: int, y: int, cell_type: str) -> None:
        """Сеттер точки лабиринта."""
        self._cells[x][y] = cell_type

    def get_cell(self, x: int, y: int) -> str:
        """Геттер точки лабиринта."""
        return self._cells[x][y]

    def console_visualize(self) -> None:
        """Консольная визуализация лабиринта."""
        visualized = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if self.is_unicode:
                    row += ASCII_TO_UNICODE[self._cells[x][y]]
                else:
                    row += self._cells[x][y]
            visualized.append(row)
        for row in visualized:
            print(row)

    def save_to_file(self, filename: str) -> None:
        """Сохраняем лабиринт в файл."""
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            for y in range(self.height):
                for x in range(self.width):
                    if self.is_unicode:
                        file.write(ASCII_TO_UNICODE[self._cells[x][y]])
                    else:
                        file.write(self._cells[x][y])
                # Ставим переход на новую строку. При считывании лабиринта
                # из файла эти переходы будет убирать
                file.write("\n")
            file.close()

    @classmethod
    def load_from_file(cls, filename: str) -> "Maze":
        """Выгружаем в список строк, удаляя переводы строки."""
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = []
        with path.open("r", encoding="utf-8") as file:
            is_unicode = file.read(1) in ASCII_TO_UNICODE.values()
            file.seek(0)
            lines = [line.strip() for line in file]
        file.close()

        height = len(lines)
        width = max(len(line) for line in lines)
        maze = cls(width, height, is_unicode=is_unicode)
        # Восстанавливаем лабиринт поэлементно
        for y in range(height):
            for x in range(width):
                if is_unicode:
                    maze.set_cell(x, y, UNICODE_TO_ASCII[lines[y][x]])
                else:
                    maze.set_cell(x, y, lines[y][x])
        return maze

    def validate_points(
        self, start_x: int, start_y: int, end_x: int, end_y: int
    ) -> None:
        """Проверка, что точки внутри лабиринта и не стены."""
        for x, y, name in [(start_x, start_y, "Стартовая"), (end_x, end_y, "Конечная")]:
            if not 0 <= x < self.width or not 0 <= y < self.height:
                message = f"{name} точка лежит вне лабиринта"
                raise ValueError(message)
            if self.get_cell(x, y) == CellType.WALL:
                message = f"{name} точка не должна быть стеной"
                raise ValueError(message)
