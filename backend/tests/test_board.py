import pytest

from backend.app.board import Board


WINS = [
    (5, [0, 5, 1, 6, 2, 7, 3, 8, 4], 1),
    (5, [0, 5, 1, 6, 2, 7, 3, 8, 10, 9], -1),
    (5, [0, 5, 1, 6, 10, 7, 3, 8, 4], 0),
    (5, [0, 5, 1, 6, 2, 7, 10, 8, 4], 0),
    (5, [0, 1, 5, 2, 10, 3, 15, 4, 20], 1),
    (5, [0, 1, 5, 2, 10, 3, 16, 4, 20], 0),
    (5, [0, 1, 5, 2, 10, 3, 16, 4, 20, 15], 0),
    (5, [0, 1, 6, 2, 12, 3, 18, 4, 24], 1),
    (5, [0, 1, 6, 2, 12, 3, 19, 4, 24], 0),
    (5, [0, 1, 6, 2, 12, 3, 19, 4, 24, 18], 0),
    (5, [4, 0, 8, 1, 12, 2, 16, 3, 20], 1),
    (5, [4, 0, 8, 1, 12, 2, 15, 3, 20], 0),
    (5, [4, 0, 8, 1, 12, 2, 16, 20], 0),
]


def test_board_initializes_empty_grid():
    board = Board(size=15)

    assert board.board == [[0 for _ in range(15)] for _ in range(15)]
    assert board.current_player == 1
    assert board.history == []


def test_put_places_piece_and_switches_player():
    board = Board(size=15)

    board.put(1, 1)

    assert board.board[1][1] == 1
    assert board.current_player == -1
    assert board.history == [{"i": 1, "j": 1, "role": 1}]


def test_put_rejects_out_of_bounds_and_occupied_cells():
    board = Board(size=3)

    assert board.put(-1, 0) is False
    assert board.put(3, 0) is False
    assert board.put(1, 1) is True
    assert board.put(1, 1) is False
    assert board.board[1][1] == 1
    assert len(board.history) == 1


def test_get_valid_moves_excludes_occupied_cells():
    board = Board(size=3)
    board.put(1, 1)

    assert [1, 1] not in board.get_valid_moves()
    assert len(board.get_valid_moves()) == 8


def test_is_game_over_detects_diagonal_win():
    board = Board(size=6)

    assert board.is_game_over() is False
    for i, j in [[0, 0], [0, 1], [1, 1], [1, 2], [2, 2], [2, 3], [3, 3], [3, 4], [4, 4]]:
        board.put(i, j)

    assert board.is_game_over() is True
    assert board.get_winner() == 1


def test_is_game_over_detects_full_board_draw():
    board = Board(size=3)

    for i in range(3):
        for j in range(3):
            board.put(i, j, 1 if (i + j) % 2 == 0 else -1)

    assert board.get_winner() == 0
    assert board.is_game_over() is True


def test_undo_removes_last_move_and_restores_player():
    board = Board(size=15)
    board.put(1, 1)

    assert board.undo() is True

    assert board.board[1][1] == 0
    assert board.current_player == 1
    assert board.history == []


def test_undo_returns_false_without_history():
    board = Board(size=15)

    assert board.undo() is False


@pytest.mark.parametrize(("size", "moves", "winner"), WINS)
def test_get_winner_matches_js_board_fixtures(size, moves, winner):
    board = Board(size=size)

    for move in moves:
        i, j = board.position_to_coordinate(move)
        board.put(i, j)

    assert board.get_winner() == winner


def test_coordinate_conversion_round_trips():
    board = Board(size=15)

    assert board.position_to_coordinate(17) == [1, 2]
    assert board.coordinate_to_position([1, 2]) == 17
