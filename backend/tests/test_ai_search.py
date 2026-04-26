import pytest

from backend.app.board import Board
from backend.app.evaluation import FIVE, FOUR, Evaluate
from backend.app.minmax import cache_hits, minmax, reset_search_cache, search_metrics, vcf, vct
from backend.app.shape import Shape, get_shape_fast
from backend.app.zobrist import Zobrist


def play(board: Board, steps: list[list[int]]) -> None:
    for i, j in steps:
        board.put(i, j)


@pytest.fixture(autouse=True)
def clear_search_cache():
    reset_search_cache()
    yield
    reset_search_cache()


def opponent_has_immediate_win(board: Board, role: int) -> bool:
    for move in board.get_valid_moves():
        board.put(move[0], move[1], role)
        is_win = board.get_winner() == role
        board.undo()
        if is_win:
            return True
    return False


def board_state(board: Board):
    return [row.copy() for row in board.board], [move.copy() for move in board.history], board.hash(), board.current_player


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

    first = minmax(board, 1, depth=2)
    assert cache_hits["total"] > 0

    second = minmax(board, 1, depth=2)

    assert cache_hits["hit"] > 0
    assert second == first


def test_search_metrics_track_nodes_depth_candidates_and_cache():
    board = Board(size=6)
    steps = [[0, 0], [0, 1], [1, 1], [1, 2], [2, 2], [2, 3], [3, 3], [3, 4]]
    play(board, steps)

    first = minmax(board, 1, depth=2)

    assert first[1] == [4, 4]
    assert search_metrics["nodes"] > 0
    assert search_metrics["leaf_nodes"] > 0
    assert search_metrics["cache_stores"] > 0
    assert search_metrics["candidate_moves"] > 0
    assert search_metrics["max_depth"] == 1
    assert search_metrics["cache_hits"] == 0

    second = minmax(board, 1, depth=2)

    assert second == first
    assert search_metrics["cache_hits"] > 0
    assert cache_hits["hit"] == search_metrics["cache_hits"]
    assert cache_hits["search"] == search_metrics["nodes"]


def test_reset_search_cache_resets_metrics():
    board = Board(size=6)
    steps = [[0, 0], [0, 1], [1, 1], [1, 2], [2, 2], [2, 3], [3, 3], [3, 4]]
    play(board, steps)
    minmax(board, 1, depth=2)

    assert any(search_metrics.values())

    reset_search_cache()

    assert search_metrics == {
        "nodes": 0,
        "cache_hits": 0,
        "cache_stores": 0,
        "prunes": 0,
        "max_depth": 0,
        "candidate_moves": 0,
        "leaf_nodes": 0,
    }
    assert cache_hits == {"search": 0, "total": 0, "hit": 0}


def test_minmax_blocks_opponent_immediate_win():
    board = Board(size=7)
    steps = [[2, 0], [2, 1], [6, 6], [2, 2], [5, 5], [2, 3], [4, 6], [2, 4]]
    play(board, steps)

    value, move, path = minmax(board, 1, depth=2)

    assert move == [2, 5]
    assert path[0] == move
    assert board.board[move[0]][move[1]] == 0
    board.put(move[0], move[1], 1)
    assert not opponent_has_immediate_win(board, -1)
    board.undo()


def test_minmax_returns_legal_move_for_opening_board():
    board = Board(size=9)

    value, move, path = minmax(board, 1, depth=1)

    assert move in board.get_valid_moves()
    assert path[0] == move
    assert board.board[move[0]][move[1]] == 0


def test_vct_prefers_open_three_candidate_set():
    board = Board(size=9)
    steps = [[4, 3], [0, 0], [4, 4], [0, 1], [5, 5], [0, 2]]
    play(board, steps)

    value, move, path = vct(board, 1, depth=1)

    assert move in ([4, 2], [4, 5], [3, 3], [6, 6])
    assert path[0] == move


def test_vcf_prefers_four_candidate_set():
    board = Board(size=9)
    steps = [[4, 2], [0, 0], [4, 3], [0, 1], [4, 4], [0, 2]]
    play(board, steps)

    value, move, path = vcf(board, 1, depth=1)

    assert move in ([4, 1], [4, 5])
    assert path[0] == move


def test_repeated_minmax_search_does_not_mutate_board_state_or_result():
    board = Board(size=9)
    steps = [[4, 4], [5, 3], [4, 5], [5, 4], [3, 5], [6, 4]]
    play(board, steps)
    before = board_state(board)

    first = minmax(board, 1, depth=2)
    after_first = board_state(board)
    second = minmax(board, 1, depth=2)

    assert after_first == before
    assert board_state(board) == before
    assert second == first


def test_vct_and_vcf_do_not_mutate_board_state():
    board = Board(size=9)
    steps = [[4, 2], [0, 0], [4, 3], [0, 1], [4, 4], [0, 2]]
    play(board, steps)
    before = board_state(board)

    vct(board, 1, depth=2)
    assert board_state(board) == before

    vcf(board, 1, depth=2)
    assert board_state(board) == before


def test_minmax_opening_has_no_forced_win():
    board = Board(size=10)
    steps = [[4, 4], [5, 3], [4, 5], [5, 4]]
    play(board, steps)

    value, move, path = minmax(board, 1, depth=2)

    assert value < FOUR
    assert move == [5, 5]
    assert path[0] == move
    assert board.board[move[0]][move[1]] == 0
