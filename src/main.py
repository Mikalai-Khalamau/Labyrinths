import argparse

from Generator import Generator
from Maze import Maze
from Solver import Solver

TWO_COORDS_LENGTH = 2


def check_coordinates(string: str) -> tuple[int, int]:
    """Проверка ввода числовых координат."""
    if "," not in string or len(string.split(",")) != TWO_COORDS_LENGTH:
        message = f"Неверный формат точки: {string}, ожидаемый формат: x,y"
        raise ValueError(message)

    try:
        x, y = map(int, string.split(","))
    except ValueError as e:
        message = f"Неверный формат точки {string}, ожидалось x,y"
        raise ValueError(message) from e

    if x < 0 or y < 0:
        message = "Координаты точки должны быть неотрицательными"
        raise ValueError(message)
    return x, y


def output_maze(maze: Maze, output: str) -> None:
    """Выбираем выводить в консоль или в файл."""
    if output:
        maze.save_to_file(output)
    else:
        maze.console_visualize()


def generate_command(args: argparse.Namespace) -> None:
    """Логика команды generate."""
    algorithm = args.algorithm
    width = args.width
    height = args.height
    generator = Generator(width, height)
    maze = None
    if algorithm not in ["prima", "dfs"]:
        message = f"Неизвестный алгоритм генерации: {algorithm}"
        raise ValueError(message)
    if algorithm == "prima":
        maze = generator.prima_generate(is_unicode=args.unicode)
    elif algorithm == "dfs":
        maze = generator.dfs_generate(is_unicode=args.unicode)
    output_maze(maze, args.output)


def solve_command(args: argparse.Namespace) -> None:
    """Логика команды solve."""
    start_x, start_y = check_coordinates(args.start)
    end_x, end_y = check_coordinates(args.end)
    algorithm = args.algorithm

    if not args.file:
        message = "--file необходим для выгрузки лабиринта и поиска пути"
        raise ValueError(message)
    file = args.file

    try:
        maze = Maze.load_from_file(file)
    except (FileNotFoundError, OSError) as e:
        message = f"Файл не удалось прочитать {e}"
        raise ValueError(message) from e
    maze.validate_points(start_x, start_y, end_x, end_y)

    solver = Solver(start_x, start_y, end_x, end_y)
    if algorithm not in ["dijkstra", "astar"]:
        message = f"Неизвестный алгоритм: {algorithm}"
        raise ValueError(message)

    if algorithm == "dijkstra":
        try:
            maze = solver.dijkstra_solve(maze)
        except (KeyError, ValueError) as e:
            message = f"Путь не найден, несвязный лабиринт {e}"
            raise ValueError(message) from e
    elif algorithm == "astar":
        try:
            maze = solver.astar_solve(maze)
        except (KeyError, ValueError) as e:
            message = f"Путь не найден, несвязный лабиринт {e}"
            raise ValueError(message) from e

    output_maze(maze, args.output)


def create_parser() -> argparse.ArgumentParser:
    """Создание парсера аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Программа для генерации и решения лабиринтов в командной строке"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Две команды: Генерация и решение.Использование: python main.py "
        "[Команда] аргумент=значение ...",
        required=True,
    )
    generate_parser = subparsers.add_parser(
        "generate",
        help="Создает лабиринт. Нужно задать алгоритм(--algorithm),"
        " ширину(--width) и высоту(--height), файл для записи(--output)"
        "(если не задать - выведет в консоль)",
    )
    solve_parser = subparsers.add_parser(
        "solve",
        help="Находит путь в лабиринте. Нужно задать файл с лабиринтом(--file),"
        " алгоритм(--algorithm), стартовую(--start) и конечную(--end) точки,"
        " выходной файл(--output)(если не задать, то в консоль)",
    )

    generate_parser.add_argument("--algorithm", required=True)
    generate_parser.add_argument("--width", required=True, type=int)
    generate_parser.add_argument("--height", required=True, type=int)
    generate_parser.add_argument(
        "--output",
        required=False,
        type=str,
        help="Файл для вывода. Если не задан - в консоль.",
    )
    generate_parser.add_argument(
        "--unicode", action="store_true", help="Использовать Unicode-символы"
    )

    solve_parser.add_argument("--algorithm", required=True)
    solve_parser.add_argument("--file", required=True, help="Файл с лабиринтом")
    solve_parser.add_argument("--start", required=True)
    solve_parser.add_argument("--end", required=True)
    solve_parser.add_argument(
        "--output",
        required=False,
        type=str,
        help="Файл для вывода. Если не задан - в консоль.",
    )

    return parser


def main() -> None:
    """Точка входа приложения."""
    parser = create_parser()
    args = parser.parse_args()
    try:
        if args.command == "generate":
            generate_command(args)
        elif args.command == "solve":
            solve_command(args)
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()
