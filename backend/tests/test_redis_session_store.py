from backend.app.board import Board
from backend.app.game import GameSession, play_ai_move, snapshot
from backend.app.redis_session_store import RedisSessionStore, deserialize_session, serialize_session


class FakeRedis:
    def __init__(self):
        self.items = {}
        self.expirations = {}

    def set(self, name: str, value: str, ex: int | None = None):
        self.items[name] = value
        self.expirations[name] = ex

    def get(self, name: str):
        return self.items.get(name)

    def delete(self, *names: str):
        for name in names:
            self.items.pop(name, None)
            self.expirations.pop(name, None)

    def keys(self, pattern: str):
        prefix = pattern.removesuffix("*")
        return [key for key in self.items if key.startswith(prefix)]


def make_session() -> GameSession:
    board = Board(size=7)
    board.put(3, 3, 1)
    board.put(3, 4, -1)
    return GameSession(
        board=board,
        ai_first=False,
        depth=1,
        last_score=12,
        last_best_path=[[2, 2], [4, 4]],
        last_current_depth=1,
        last_search_metrics={"nodes": 3, "beta_cutoffs": 1, "cache_hits": 0, "cache_stores": 1, "candidate_moves": 4, "leaf_nodes": 2, "max_depth": 1, "elapsed_ms": 1.5},
    )


def test_redis_session_serialization_round_trips_board_and_ai_state():
    session = make_session()

    restored = deserialize_session(serialize_session(session))

    assert restored.board.size == session.board.size
    assert restored.board.board == session.board.board
    assert restored.board.history == session.board.history
    assert restored.board.current_player == session.board.current_player
    assert restored.board.hash() == session.board.hash()
    assert restored.ai_first is False
    assert restored.depth == 1
    assert restored.last_score == 12
    assert restored.last_best_path == [[2, 2], [4, 4]]
    assert restored.last_current_depth == 1
    assert restored.last_search_metrics["nodes"] == 3
    assert restored.last_search_metrics["elapsed_ms"] == 1.5


def test_redis_session_store_creates_reads_updates_and_removes_sessions():
    redis = FakeRedis()
    store = RedisSessionStore(redis, ttl_seconds=30, key_prefix="test:")
    session_id = store.create(make_session())

    assert len(store) == 1
    assert redis.expirations[f"test:{session_id}"] == 30
    assert session_id in store
    assert store.get(session_id).board.history == [{"i": 3, "j": 3, "role": 1}, {"i": 3, "j": 4, "role": -1}]

    result = store.with_session(session_id, lambda session: session.board.put(2, 2, session.board.current_player))

    assert result is True
    assert store.get(session_id).board.history[-1] == {"i": 2, "j": 2, "role": 1}

    removed = store.remove(session_id)

    assert removed.board.history[-1] == {"i": 2, "j": 2, "role": 1}
    assert store.get(session_id) is None
    assert len(store) == 0


def test_redis_session_store_with_session_can_remove_after_snapshot_action():
    store = RedisSessionStore(FakeRedis(), key_prefix="test:")
    session_id = store.create(make_session())

    result = store.with_session(session_id, lambda session: len(session.board.history), remove=True)

    assert result == 2
    assert store.get(session_id) is None


def test_redis_backend_supports_start_move_undo_end_lifecycle():
    store = RedisSessionStore(FakeRedis(), key_prefix="test:")
    session = GameSession(board=Board(size=6), ai_first=False, depth=1)
    session_id = store.create(session)

    started = store.get(session_id)

    assert snapshot(session_id, started)["size"] == 6

    moved = store.with_session(
        session_id,
        lambda active: active.board.put(2, 2, active.board.current_player) and play_ai_move(active, depth=1),
    )
    after_move = store.get(session_id)

    assert moved is True
    assert len(after_move.board.history) == 2

    undone = store.with_session(session_id, lambda active: [active.board.undo() for _ in range(min(2, len(active.board.history)))])
    after_undo = store.get(session_id)

    assert undone == [True, True]
    assert after_undo.board.history == []

    ended = store.with_session(session_id, lambda active: snapshot(session_id, active), remove=True)

    assert ended["session_id"] == session_id
    assert store.get(session_id) is None

