from time import perf_counter

import pytest

from backend.app.board import Board
from backend.app.evaluation import FIVE
from backend.app.minmax import cache_hits, minmax, reset_search_cache, search_metrics


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


def assert_smoke_budget(elapsed_seconds: float, *, max_nodes: int, max_candidates: int) -> None:
    assert elapsed_seconds < 2.0
    assert 0 < search_metrics["nodes"] <= max_nodes
    assert 0 < search_metrics["candidate_moves"] <= max_candidates
    assert search_metrics["max_depth"] <= 2


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
    assert_smoke_budget(elapsed, max_nodes=160, max_candidates=180)


def test_midgame_tactical_search_stays_within_smoke_budget_and_uses_cache():
    board = Board(size=9)
    play(board, [[4, 4], [5, 3], [4, 5], [5, 4], [3, 5], [6, 4]])

    (value, move, path), elapsed = timed_minmax(board, 1, depth=2)

    assert move in board.get_valid_moves()
    assert path[0] == move
    assert board.board[move[0]][move[1]] == 0
    assert_smoke_budget(elapsed, max_nodes=260, max_candidates=320)

    minmax(board, 1, depth=2)

    assert cache_hits["hit"] > 0
    assert search_metrics["cache_hits"] > 0
