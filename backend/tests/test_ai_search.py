from backend.app.board import Board
from backend.app.evaluation import FIVE, FOUR, Evaluate
from backend.app.minmax import cache_hits, minmax, reset_search_cache, vcf, vct
from backend.app.shape import Shape, get_shape_fast
from backend.app.zobrist import Zobrist


def play(board: Board, steps: list[list[int]]) -> None:
    for i, j in steps:
        board.put(i, j)


def test_zobrist_hash_is_deterministic_and_undoable():
    first = Zobrist(size=15, seed=20231123)
    second = Zobrist(size=15, seed=20231123)

    assert first.current_hash == second.current_hash == 0

    first.toggle_piece(7, 7, 1)
    second.toggle_piece(7, 7, 1)

    assert first.current_hash == second.current_hash

    first.toggle_piece(7, 7, 1)

    assert first.current_hash == 0


def test_shape_fast_detects_open_four_from_js_fixture():
    board = Board(size=9)
    steps = [[3, 1], [3, 0], [3, 2], [6, 2], [3, 3], [6, 3], [4, 3], [6, 4], [5, 2], [7, 2], [3, 4]]
    play(board, steps)

    shape, _ = get_shape_fast(board.board, 2, 5, -1, 1, 1)

    assert shape == Shape.FOUR


def test_evaluator_prioritizes_fives_and_block_fives():
    evaluator = Evaluate(size=15)
    steps = [[6, 6], [7, 6], [6, 7], [7, 7], [6, 8], [7, 9], [6, 9], [7, 10]]
    for index, (i, j) in enumerate(steps):
        evaluator.move(i, j, 1 if index % 2 == 0 else -1)

    assert evaluator.evaluate(1) < FOUR
    assert evaluator.get_moves(1) == [[6, 5], [6, 10], [7, 8]]


def test_board_evaluate_returns_five_for_existing_winner():
    board = Board(size=6)
    steps = [[0, 0], [0, 1], [1, 1], [1, 2], [2, 2], [2, 3], [3, 3], [3, 4], [4, 4]]
    play(board, steps)

    assert board.evaluate(1) == FIVE
    assert board.evaluate(-1) == -FIVE


def test_minmax_finds_immediate_win():
    board = Board(size=6)
    steps = [[0, 0], [0, 1], [1, 1], [1, 2], [2, 2], [2, 3], [3, 3], [3, 4]]
    play(board, steps)

    value, move, path = minmax(board, 1, depth=2)

    assert value == FIVE
    assert move == [4, 4]
    assert path[0] == [4, 4]


def test_vct_and_vcf_find_immediate_win():
    board = Board(size=6)
    steps = [[0, 0], [0, 1], [1, 1], [1, 2], [2, 2], [2, 3], [3, 3], [3, 4]]
    play(board, steps)

    assert vct(board, 1, depth=2)[0:2] == [FIVE, [4, 4]]
    assert vcf(board, 1, depth=2)[0:2] == [FIVE, [4, 4]]


def test_minmax_uses_zobrist_cache_on_repeated_search():
    reset_search_cache()
    board = Board(size=6)
    steps = [[0, 0], [0, 1], [1, 1], [1, 2], [2, 2], [2, 3], [3, 3], [3, 4]]
    play(board, steps)

    minmax(board, 1, depth=2)
    assert cache_hits["total"] > 0

    minmax(board, 1, depth=2)

    assert cache_hits["hit"] > 0


def test_minmax_opening_has_no_forced_win():
    board = Board(size=10)
    steps = [[4, 4], [5, 3], [4, 5], [5, 4]]
    play(board, steps)

    value, move, path = minmax(board, 1, depth=2)

    assert value < FOUR
    assert move in board.get_valid_moves()
    assert path
