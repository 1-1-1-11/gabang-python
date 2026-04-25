from enum import IntEnum


class Shape(IntEnum):
    NONE = 0
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    TWO_TWO = 22
    BLOCK_THREE = 30
    THREE_THREE = 33
    BLOCK_FOUR = 40
    FOUR_THREE = 43
    FOUR_FOUR = 44
    BLOCK_FIVE = 50


DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))


def is_five(shape: int) -> bool:
    return shape in (Shape.FIVE, Shape.BLOCK_FIVE)


def is_four(shape: int) -> bool:
    return shape in (Shape.FOUR, Shape.BLOCK_FOUR)


def get_shape_fast(board: list[list[int]], x: int, y: int, offset_x: int, offset_y: int, role: int) -> tuple[Shape, int]:
    if board[x][y] != 0:
        return Shape.NONE, 1

    if (
        _cell(board, x + offset_x, y + offset_y) == 0
        and _cell(board, x - offset_x, y - offset_y) == 0
        and _cell(board, x + 2 * offset_x, y + 2 * offset_y) == 0
        and _cell(board, x - 2 * offset_x, y - 2 * offset_y) == 0
    ):
        return Shape.NONE, 1

    line = _line_string(board, x, y, offset_x, offset_y, role)
    contiguous = _contiguous_count(board, x, y, offset_x, offset_y, role)

    if "11111" in line:
        open_ended = _has_open_end(board, x, y, offset_x, offset_y, role, -1) and _has_open_end(
            board, x, y, offset_x, offset_y, role, 1
        )
        return (Shape.FIVE if open_ended else Shape.BLOCK_FIVE), contiguous
    if "011110" in line:
        return Shape.FOUR, contiguous
    if any(pattern in line for pattern in ("10111", "11011", "11101", "211110", "211101", "211011", "210111", "011112", "101112", "110112", "111012")):
        return Shape.BLOCK_FOUR, contiguous
    if any(pattern in line for pattern in ("011100", "011010", "010110", "001110")):
        return Shape.THREE, contiguous
    if any(pattern in line for pattern in ("211100", "211010", "210110", "001112", "010112", "011012")):
        return Shape.BLOCK_THREE, contiguous
    if any(pattern in line for pattern in ("001100", "011000", "000110", "010100", "001010")):
        return Shape.TWO, contiguous
    return Shape.NONE, contiguous


def _line_string(board: list[list[int]], x: int, y: int, dx: int, dy: int, role: int) -> str:
    values: list[str] = []
    for step in range(-5, 6):
        i = x + step * dx
        j = y + step * dy
        if step == 0:
            values.append("1")
            continue
        value = _cell(board, i, j)
        if value == role:
            values.append("1")
        elif value == 0:
            values.append("0")
        else:
            values.append("2")
    return "".join(values)


def _contiguous_count(board: list[list[int]], x: int, y: int, dx: int, dy: int, role: int) -> int:
    total = 1
    for sign in (-1, 1):
        step = 1
        while _cell(board, x + sign * step * dx, y + sign * step * dy) == role:
            total += 1
            step += 1
    return total


def _has_open_end(board: list[list[int]], x: int, y: int, dx: int, dy: int, role: int, sign: int) -> bool:
    step = 1
    while _cell(board, x + sign * step * dx, y + sign * step * dy) == role:
        step += 1
    return _cell(board, x + sign * step * dx, y + sign * step * dy) == 0


def _cell(board: list[list[int]], i: int, j: int) -> int:
    if i < 0 or j < 0 or i >= len(board) or j >= len(board):
        return 2
    return board[i][j]
