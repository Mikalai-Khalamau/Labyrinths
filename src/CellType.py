from enum import StrEnum


class CellType(StrEnum):
    """Тип ячейки в лабиринте - стена, пустота, путь, старт, конец."""

    WALL = "#"
    PASSABLE = " "
    ROAD = "."
    START = "O"
    END = "X"


ASCII_TO_UNICODE = {
    CellType.WALL: "\U000025A0",
    CellType.PASSABLE: "\U000025A1",
    CellType.ROAD: "\U000000B7",
    CellType.START: "\U000025CB",
    CellType.END: "\U000025CE",
}

UNICODE_TO_ASCII = {
    "\U000025A0": CellType.WALL,
    "\U000025A1": CellType.PASSABLE,
    "\U000000B7": CellType.ROAD,
    "\U000025CB": CellType.START,
    "\U000025CE": CellType.END,
}
