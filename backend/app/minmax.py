from dataclasses import dataclass
from typing import Literal

from backend.app.cache import Cache
from backend.app.evaluation import FIVE

MAX = 1_000_000_000
CacheBound = Literal["exact", "lower", "upper"]


@dataclass(frozen=True)
class CacheEntry:
    value: int
    move: list[int] | None
    path: list[list[int]]
    bound: CacheBound


cache_hits = {"search": 0, "total": 0, "hit": 0}
search_metrics = {
    "nodes": 0,
    "cache_hits": 0,
    "cache_stores": 0,
    "prunes": 0,
    "max_depth": 0,
    "candidate_moves": 0,
    "leaf_nodes": 0,
}
_cache = Cache()


def minmax(board, role: int, depth: int = 4):
    return _search(board, role, depth, 0, [], -MAX, MAX)


def vct(board, role: int, depth: int = 8):
    return _search(board, role, depth, 0, [], -MAX, MAX, only_three=True)


def vcf(board, role: int, depth: int = 8):
    return _search(board, role, depth, 0, [], -MAX, MAX, only_four=True)


def _search(board, role: int, depth: int, current_depth: int, path: list[list[int]], alpha: int, beta: int, only_three: bool = False, only_four: bool = False):
    cache_hits["search"] += 1
    search_metrics["nodes"] += 1
    search_metrics["max_depth"] = max(search_metrics["max_depth"], current_depth)
    if current_depth >= depth or board.is_game_over():
        search_metrics["leaf_nodes"] += 1
        return [board.evaluate(role), None, path.copy()]

    cache_key = _build_cache_key(board, role, depth - current_depth, only_three, only_four)
    cached = _cache.get(cache_key)
    if cached is not None:
        cached_result = _cached_result(cached, alpha, beta, path)
        if cached_result is not None:
            cache_hits["hit"] += 1
            search_metrics["cache_hits"] += 1
            return cached_result

    moves = board.get_valuable_moves(role, current_depth, only_three, only_four)
    search_metrics["candidate_moves"] += len(moves)
    if not moves:
        search_metrics["leaf_nodes"] += 1
        return [board.evaluate(role), None, path.copy()]

    alpha_start = alpha
    value = -MAX
    best_move = None
    best_path = path.copy()

    for move in moves:
        board.put(move[0], move[1], role)
        current_value, _, current_path = _search(board, -role, depth, current_depth + 1, path + [move], -beta, -alpha, only_three, only_four)
        current_value = -current_value
        board.undo()

        if current_value > value:
            value = current_value
            best_move = move
            best_path = current_path
        alpha = max(alpha, value)
        if alpha >= beta or alpha >= FIVE:
            search_metrics["prunes"] += 1
            break

    remaining_path = best_path[current_depth:]
    # FIVE is the terminal win ceiling, so a FIVE early stop is exact unless the beta window says otherwise.
    bound = _cache_bound(value, alpha_start, beta)
    _cache.put(cache_key, CacheEntry(value=value, move=best_move, path=remaining_path, bound=bound))
    cache_hits["total"] += 1
    search_metrics["cache_stores"] += 1
    return [value, best_move, best_path]


def reset_search_cache() -> None:
    _cache.clear()
    cache_hits.update({"search": 0, "total": 0, "hit": 0})
    reset_search_metrics()


def reset_search_metrics() -> None:
    search_metrics.update(
        {
            "nodes": 0,
            "cache_hits": 0,
            "cache_stores": 0,
            "prunes": 0,
            "max_depth": 0,
            "candidate_moves": 0,
            "leaf_nodes": 0,
        }
    )


def _build_cache_key(board, role: int, remaining_depth: int, only_three: bool, only_four: bool):
    return (board.size, board.hash(), role, remaining_depth, only_three, only_four)


def _cache_bound(value: int, alpha: int, beta: int) -> CacheBound:
    if value <= alpha:
        return "upper"
    if value >= beta:
        return "lower"
    return "exact"


def _cached_result(entry: CacheEntry, alpha: int, beta: int, path: list[list[int]]) -> list | None:
    if entry.bound == "exact":
        return [entry.value, entry.move, path + entry.path]
    if entry.bound == "lower" and entry.value >= beta:
        return [entry.value, entry.move, path + entry.path]
    if entry.bound == "upper" and entry.value <= alpha:
        return [entry.value, entry.move, path + entry.path]
    return None
