from time import perf_counter

import pytest

from backend.app.board import Board
from backend.app.evaluation import FIVE
from backend.app.minmax import cache_hits, minmax, reset_search_cache, search_metrics

CORE_METRIC_KEYS = {
    "nodes",
    "cache_hits",
    "cache_stores",
    "beta_cutoffs",
    "max_depth",
    "candidate_moves",
    "leaf_nodes",
}


def play(board: Board, steps: list[list[int]]) -> None:
    for i, j in steps:
        board.put(i, j)


@pytest.fixture(autouse=True)
def clear_search_cache():
    reset_search_cache()
    yield
    reset_search_cache()


def timed_minmax(board: Board, role: int, depth: int):
    started_at = perf_counter()
    result = minmax(board, role, depth=depth)
    return result, perf_counter() - started_at


def metric_snapshot() -> dict[str, int]:
    return {key: search_metrics[key] for key in sorted(search_metrics)}


def assert_smoke_budget(elapsed_seconds: float, *, max_nodes: int, max_candidates: int, max_depth: int = 2) -> None:
    snapshot = metric_snapshot()

    assert elapsed_seconds < 2.0
    assert set(snapshot) == CORE_METRIC_KEYS
    assert 0 < snapshot["nodes"] <= max_nodes
    assert 0 < snapshot["candidate_moves"] <= max_candidates
    assert snapshot["leaf_nodes"] > 0
    assert snapshot["cache_stores"] > 0
    assert snapshot["max_depth"] <= max_depth


def test_opening_search_records_center_baseline():
    board = Board(size=9)

    (value, move, path), elapsed = timed_minmax(board, 1, depth=1)

    assert value > 0
    assert move == [4, 4]
    assert path == [[4, 4]]
    assert_smoke_budget(elapsed, max_nodes=5, max_candidates=5, max_depth=1)


def test_immediate_win_stays_within_smoke_budget():
    board = Board(size=6)
    play(board, [[0, 0], [0, 1], [1, 1], [1, 2], [2, 2], [2, 3], [3, 3], [3, 4]])

    (value, move, path), elapsed = timed_minmax(board, 1, depth=2)

    assert value == FIVE
    assert move == [4, 4]
    assert path[0] == move
    assert_smoke_budget(elapsed, max_nodes=80, max_candidates=80)


def test_must_block_stays_within_smoke_budget():
    board = Board(size=7)
    play(board, [[2, 0], [2, 1], [6, 6], [2, 2], [5, 5], [2, 3], [4, 6], [2, 4]])

    (value, move, path), elapsed = timed_minmax(board, 1, depth=2)

    assert move == [2, 5]
    assert path[0] == move
    assert_smoke_budget(elapsed, max_nodes=160, max_candidates=120)


def test_simple_threat_sequence_stays_within_smoke_budget():
    board = Board(size=9)
    play(board, [[4, 2], [0, 0], [4, 3], [0, 1], [4, 4], [0, 2]])

    (value, move, path), elapsed = timed_minmax(board, 1, depth=2)

    assert value > 0
    assert move in ([4, 1], [4, 5])
    assert path[0] == move
    assert len(path) >= 2
    assert_smoke_budget(elapsed, max_nodes=80, max_candidates=80, max_depth=3)


def test_midgame_tactical_search_stays_within_smoke_budget_and_uses_cache():
    board = Board(size=9)
    play(board, [[4, 4], [5, 3], [4, 5], [5, 4], [3, 5], [6, 4]])

    (value, move, path), elapsed = timed_minmax(board, 1, depth=2)

    assert move in board.get_valid_moves()
    assert path[0] == move
    assert board.board[move[0]][move[1]] == 0
    assert_smoke_budget(elapsed, max_nodes=260, max_candidates=500, max_depth=3)

    minmax(board, 1, depth=2)

    assert cache_hits["hit"] > 0
    assert search_metrics["cache_hits"] > 0
