import pytest

from backend.app.board import Board
from backend.app.evaluation import FIVE, FOUR, Evaluate
from backend.app.minmax import (
    CacheEntry,
    _cache_bound,
    _cached_result,
    cache_hits,
    minmax,
    reset_search_cache,
    search_metrics,
    vcf,
    vct,
)
from backend.app.shape import Shape, get_shape_fast
from backend.app.zobrist import Zobrist


def play(board: Board, steps: list[list[int]]) -> None:
    for i, j in steps:
        board.put(i, j)


def play_roles(board: Board, steps: list[tuple[int, int, int]]) -> None:
    for i, j, role in steps:
        assert board.put(i, j, role)


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


def test_evaluator_orders_own_immediate_win_before_defensive_block():
    evaluator = Evaluate(size=9)
    for i, j, role in [
        (2, 0, -1),
        (2, 1, -1),
        (2, 2, -1),
        (2, 3, -1),
        (6, 4, 1),
        (6, 5, 1),
        (6, 6, 1),
        (6, 7, 1),
    ]:
        evaluator.move(i, j, role)

    moves = evaluator.get_moves(1)

    assert moves[:2] == [[6, 3], [6, 8]]
    assert [2, 4] in moves


def test_evaluator_limits_candidate_scan_to_nearby_empty_points():
    evaluator = Evaluate(size=15)

    assert evaluator._candidate_points() == [7 * 15 + 7]

    for i, j, role in [(7, 7, 1), (2, 2, -1), (12, 12, 1)]:
        evaluator.move(i, j, role)

    candidates = evaluator._candidate_points()

    assert 0 < len(candidates) < 15 * 15 - 3
    assert evaluator.board[7][7] == 1
    assert 7 * 15 + 7 not in candidates
    assert 7 * 15 + 8 in candidates
    assert 2 * 15 + 3 in candidates
    assert 12 * 15 + 11 in candidates


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


@pytest.mark.parametrize(
    ("steps", "expected_move"),
    [
        ([[3, 0], [0, 0], [3, 1], [0, 1], [3, 2], [0, 2], [3, 3], [1, 0]], [3, 4]),
        ([[0, 4], [0, 0], [1, 4], [0, 1], [2, 4], [0, 2], [3, 4], [1, 0]], [4, 4]),
        ([[4, 0], [6, 6], [3, 1], [6, 5], [2, 2], [6, 4], [1, 3], [5, 6]], [0, 4]),
    ],
)
def test_minmax_finds_forced_immediate_win_across_directions(steps, expected_move):
    board = Board(size=7)
    play(board, steps)

    value, move, path = minmax(board, 1, depth=2)

    assert value == FIVE
    assert move == expected_move
    assert path[0] == expected_move


def test_minmax_prioritizes_own_win_before_block_for_early_prune():
    board = Board(size=9)
    play_roles(
        board,
        [
            (2, 0, -1),
            (2, 1, -1),
            (2, 2, -1),
            (2, 3, -1),
            (6, 4, 1),
            (6, 5, 1),
            (6, 6, 1),
            (6, 7, 1),
        ],
    )

    value, move, path = minmax(board, 1, depth=2)

    assert value == FIVE
    assert move == [6, 3]
    assert path[0] == move
    assert search_metrics["nodes"] == 2
    assert search_metrics["prunes"] == 1


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


def test_cache_entry_bounds_control_reuse_by_search_window():
    exact = CacheEntry(value=30, move=[1, 1], path=[[1, 1]], bound="exact")
    lower = CacheEntry(value=30, move=[2, 2], path=[[2, 2]], bound="lower")
    upper = CacheEntry(value=-30, move=[3, 3], path=[[3, 3]], bound="upper")

    assert _cache_bound(value=-30, alpha=-30, beta=30) == "upper"
    assert _cache_bound(value=30, alpha=-30, beta=30) == "lower"
    assert _cache_bound(value=0, alpha=-30, beta=30) == "exact"
    assert _cache_bound(value=FIVE, alpha=-1_000_000_000, beta=1_000_000_000) == "exact"
    assert _cached_result(exact, alpha=-100, beta=100, path=[[0, 0]]) == [30, [1, 1], [[0, 0], [1, 1]]]
    assert _cached_result(lower, alpha=-100, beta=31, path=[]) is None
    assert _cached_result(lower, alpha=-100, beta=30, path=[]) == [30, [2, 2], [[2, 2]]]
    assert _cached_result(upper, alpha=-31, beta=100, path=[]) is None
    assert _cached_result(upper, alpha=-30, beta=100, path=[]) == [-30, [3, 3], [[3, 3]]]


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


@pytest.mark.parametrize(
    ("steps", "expected_move"),
    [
        ([(3, 0, 1), (3, 1, -1), (3, 2, -1), (3, 3, -1), (3, 4, -1)], [3, 5]),
        ([(0, 3, 1), (1, 3, -1), (2, 3, -1), (3, 3, -1), (4, 3, -1)], [5, 3]),
        ([(0, 6, 1), (1, 5, -1), (2, 4, -1), (3, 3, -1), (4, 2, -1)], [5, 1]),
    ],
)
def test_minmax_blocks_forced_opponent_win_across_directions(steps, expected_move):
    board = Board(size=7)
    play_roles(board, steps)

    value, move, path = minmax(board, 1, depth=2)

    assert move == expected_move
    assert path[0] == expected_move
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


@pytest.mark.parametrize(
    ("search", "steps", "expected_path"),
    [
        (minmax, [[4, 2], [0, 0], [4, 3], [0, 1], [4, 4], [0, 2]], [[4, 5], [4, 6]]),
        (vct, [[4, 3], [0, 0], [4, 4], [0, 1], [5, 5], [0, 2]], [[3, 3], [2, 2]]),
        (vcf, [[5, 3], [0, 0], [4, 4], [0, 1], [3, 5], [0, 2]], [[2, 6], [6, 2]]),
    ],
)
def test_searches_return_expected_continuous_threat_paths(search, steps, expected_path):
    board = Board(size=9)
    play(board, steps)

    value, move, path = search(board, 1, depth=2)

    assert value > 0
    assert move == expected_path[0]
    assert path[:2] == expected_path


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
