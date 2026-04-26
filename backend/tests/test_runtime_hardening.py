from time import monotonic

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


def test_cors_origins_are_configurable(monkeypatch):
    monkeypatch.setenv("GOBANG_CORS_ORIGINS", "https://gobang.example, http://localhost:5173 ")

    assert get_cors_origins() == ["https://gobang.example", "http://localhost:5173"]


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
