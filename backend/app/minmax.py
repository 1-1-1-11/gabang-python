from backend.app.cache import Cache
from backend.app.evaluation import FIVE

MAX = 1_000_000_000

cache_hits = {"search": 0, "total": 0, "hit": 0}
_cache = Cache()


def minmax(board, role: int, depth: int = 4, enable_vct: bool = True):
    return _search(board, role, depth, 0, [], -MAX, MAX)


def vct(board, role: int, depth: int = 8):
    return _search(board, role, depth, 0, [], -MAX, MAX, only_three=True)


def vcf(board, role: int, depth: int = 8):
    return _search(board, role, depth, 0, [], -MAX, MAX, only_four=True)


def _search(board, role: int, depth: int, current_depth: int, path: list[list[int]], alpha: int, beta: int, only_three: bool = False, only_four: bool = False):
    cache_hits["search"] += 1
    if current_depth >= depth or board.is_game_over():
        return [board.evaluate(role), None, path.copy()]

    cache_key = _build_cache_key(board, role, depth - current_depth, only_three, only_four)
    cached = _cache.get(cache_key)
    if cached is not None:
        cache_hits["hit"] += 1
        cached_value, cached_move, cached_path = cached
        return [cached_value, cached_move, path + cached_path]

    moves = board.get_valuable_moves(role, current_depth, only_three, only_four)
    if not moves:
        return [board.evaluate(role), None, path.copy()]

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
            break

    remaining_path = best_path[current_depth:]
    _cache.put(cache_key, (value, best_move, remaining_path))
    cache_hits["total"] += 1
    return [value, best_move, best_path]


def reset_search_cache() -> None:
    _cache.clear()
    cache_hits.update({"search": 0, "total": 0, "hit": 0})


def _build_cache_key(board, role: int, remaining_depth: int, only_three: bool, only_four: bool):
    return (board.size, board.hash(), role, remaining_depth, only_three, only_four)
