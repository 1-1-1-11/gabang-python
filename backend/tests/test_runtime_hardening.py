from threading import Event, Thread
from time import monotonic, sleep

from fastapi.testclient import TestClient

from backend.app.board import Board
from backend.app.game import GameSession, SessionStore
from backend.app.main import app
from backend.app.minmax import _build_cache_key
from backend.app.settings import get_cors_origins


def test_session_store_expires_old_sessions():
    store = SessionStore(max_sessions=4, ttl_seconds=0.01, clock=monotonic)
    session_id = store.create(GameSession(board=Board(size=5), ai_first=False, depth=1))

    assert store.get(session_id) is not None

    store._clock = lambda: monotonic() + 1

    assert store.get(session_id) is None
    assert len(store) == 0


def test_session_store_evicts_oldest_session_with_locking_boundary():
    store = SessionStore(max_sessions=2, ttl_seconds=60)
    first = store.create(GameSession(board=Board(size=5), ai_first=False, depth=1))
    second = store.create(GameSession(board=Board(size=5), ai_first=False, depth=1))
    third = store.create(GameSession(board=Board(size=5), ai_first=False, depth=1))

    assert first not in store
    assert second in store
    assert third in store
    assert len(store) == 2


def test_session_store_serializes_same_session_actions():
    store = SessionStore(max_sessions=2, ttl_seconds=60)
    session_id = store.create(GameSession(board=Board(size=5), ai_first=False, depth=1))
    entered = Event()
    release = Event()
    order = []

    def first_action(session):
        order.append("first-entered")
        entered.set()
        release.wait(timeout=1)
        session.board.put(0, 0)
        order.append("first-leaving")

    def second_action(session):
        order.append(f"second-history-{len(session.board.history)}")

    first = Thread(target=lambda: store.with_session(session_id, first_action))
    second = Thread(target=lambda: store.with_session(session_id, second_action))

    first.start()
    assert entered.wait(timeout=1)
    second.start()
    sleep(0.02)

    assert order == ["first-entered"]

    release.set()
    first.join(timeout=1)
    second.join(timeout=1)

    assert order == ["first-entered", "first-leaving", "second-history-1"]


def test_session_store_can_remove_while_holding_session_lock():
    store = SessionStore(max_sessions=2, ttl_seconds=60)
    session = GameSession(board=Board(size=5), ai_first=False, depth=1)
    session_id = store.create(session)

    result = store.with_session(session_id, lambda active: active is session, remove=True)

    assert result is True
    assert store.get(session_id) is None


def test_cors_origins_are_configurable(monkeypatch):
    monkeypatch.setenv("GOBANG_CORS_ORIGINS", "https://gobang.example, http://localhost:5173 ")

    assert get_cors_origins() == ["https://gobang.example", "http://localhost:5173"]


def test_cors_origins_default_to_wildcard(monkeypatch):
    monkeypatch.delenv("GOBANG_CORS_ORIGINS", raising=False)

    assert get_cors_origins() == ["*"]


def test_cors_origins_blank_value_falls_back_to_wildcard(monkeypatch):
    monkeypatch.setenv("GOBANG_CORS_ORIGINS", " ,  ")

    assert get_cors_origins() == ["*"]


def test_move_rejects_negative_and_out_of_board_coordinates():
    client = TestClient(app)
    session_id = client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1}).json()["session_id"]

    negative = client.post(f"/api/games/{session_id}/move", json={"position": [-1, 2], "depth": 1})
    out_of_board = client.post(f"/api/games/{session_id}/move", json={"position": [6, 2], "depth": 1})

    assert negative.status_code == 422
    assert out_of_board.status_code == 400
    assert out_of_board.json() == {"detail": "Move position outside board."}


def test_search_cache_key_includes_board_size():
    small = Board(size=6)
    large = Board(size=7)

    assert _build_cache_key(small, 1, 2, False, False) != _build_cache_key(large, 1, 2, False, False)
