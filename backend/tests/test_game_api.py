from fastapi.testclient import TestClient
import pytest

from backend.app.game import MAX_SESSIONS, get_session, sessions
from backend.app.main import app


@pytest.fixture(autouse=True)
def clear_sessions():
    sessions.clear()
    yield
    sessions.clear()


def test_start_creates_empty_game_session():
    client = TestClient(app)

    response = client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1})

    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"]
    assert payload["size"] == 6
    assert payload["winner"] == 0
    assert payload["current_player"] == 1
    assert payload["history"] == []
    assert payload["score"] == 0
    assert payload["best_path"] == []
    assert payload["current_depth"] == 0
    assert payload["board"] == [[0 for _ in range(6)] for _ in range(6)]


def test_start_can_let_ai_move_first():
    client = TestClient(app)

    response = client.post("/api/games/start", json={"size": 6, "ai_first": True, "depth": 1})

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["history"]) == 1
    assert payload["history"][0]["role"] == 1
    assert payload["current_player"] == -1
    assert sum(cell != 0 for row in payload["board"] for cell in row) == 1


def test_move_places_player_move_and_ai_reply():
    client = TestClient(app)
    session_id = client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1}).json()["session_id"]

    response = client.post(f"/api/games/{session_id}/move", json={"position": [2, 2], "depth": 1})

    assert response.status_code == 200
    payload = response.json()
    assert payload["board"][2][2] == 1
    assert len(payload["history"]) == 2
    assert payload["history"][0] == {"i": 2, "j": 2, "role": 1}
    assert payload["history"][1]["role"] == -1
    assert payload["current_player"] == 1
    assert payload["current_depth"] == 1
    assert payload["best_path"]


def test_undo_reverts_player_and_ai_moves():
    client = TestClient(app)
    session_id = client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1}).json()["session_id"]
    client.post(f"/api/games/{session_id}/move", json={"position": [2, 2], "depth": 1})

    response = client.post(f"/api/games/{session_id}/undo")

    assert response.status_code == 200
    payload = response.json()
    assert payload["history"] == []
    assert payload["current_player"] == 1
    assert all(cell == 0 for row in payload["board"] for cell in row)


def test_undo_reverts_single_ai_first_move():
    client = TestClient(app)
    session_id = client.post("/api/games/start", json={"size": 6, "ai_first": True, "depth": 1}).json()["session_id"]

    response = client.post(f"/api/games/{session_id}/undo")

    assert response.status_code == 200
    payload = response.json()
    assert payload["history"] == []
    assert payload["current_player"] == 1
    assert all(cell == 0 for row in payload["board"] for cell in row)


def test_end_releases_game_session():
    client = TestClient(app)
    session_id = client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1}).json()["session_id"]

    response = client.post(f"/api/games/{session_id}/end")

    assert response.status_code == 200
    assert response.json()["session_id"] == session_id
    assert client.post(f"/api/games/{session_id}/undo").status_code == 404


def test_unknown_session_operations_return_not_found():
    client = TestClient(app)

    assert client.post("/api/games/not-found/move", json={"position": [2, 2], "depth": 1}).status_code == 404
    assert client.post("/api/games/not-found/undo").status_code == 404
    assert client.post("/api/games/not-found/end").status_code == 404


def test_operations_after_end_return_not_found():
    client = TestClient(app)
    session_id = client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1}).json()["session_id"]

    assert client.post(f"/api/games/{session_id}/end").status_code == 200

    assert client.post(f"/api/games/{session_id}/move", json={"position": [2, 2], "depth": 1}).status_code == 404
    assert client.post(f"/api/games/{session_id}/undo").status_code == 404
    assert client.post(f"/api/games/{session_id}/end").status_code == 404


def test_invalid_move_does_not_mutate_existing_session():
    client = TestClient(app)
    session_id = client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1}).json()["session_id"]
    before = get_session(session_id)
    assert before is not None
    before_board = [row.copy() for row in before.board.board]
    before_history = [move.copy() for move in before.board.history]
    before_hash = before.board.hash()
    before_current_player = before.board.current_player

    response = client.post(f"/api/games/{session_id}/move", json={"position": [6, 2], "depth": 1})

    after = get_session(session_id)
    assert response.status_code == 400
    assert after is before
    assert after.board.board == before_board
    assert after.board.history == before_history
    assert after.board.hash() == before_hash
    assert after.board.current_player == before_current_player


def test_occupied_move_does_not_mutate_existing_session():
    client = TestClient(app)
    session_id = client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1}).json()["session_id"]
    session = get_session(session_id)
    assert session is not None
    session.board.put(2, 2, session.board.current_player)
    before_board = [row.copy() for row in session.board.board]
    before_history = [move.copy() for move in session.board.history]
    before_hash = session.board.hash()
    before_current_player = session.board.current_player

    response = client.post(f"/api/games/{session_id}/move", json={"position": [2, 2], "depth": 1})

    after = get_session(session_id)
    assert response.status_code == 400
    assert after is session
    assert after.board.board == before_board
    assert after.board.history == before_history
    assert after.board.hash() == before_hash
    assert after.board.current_player == before_current_player


def test_move_rejects_unknown_session_and_occupied_position():
    client = TestClient(app)

    missing = client.post("/api/games/not-found/move", json={"position": [2, 2], "depth": 1})
    assert missing.status_code == 404

    session_id = client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1}).json()["session_id"]
    client.post(f"/api/games/{session_id}/move", json={"position": [2, 2], "depth": 1})
    occupied = client.post(f"/api/games/{session_id}/move", json={"position": [2, 2], "depth": 1})

    assert occupied.status_code == 400


def test_move_rejects_finished_game():
    client = TestClient(app)
    session_id = client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1}).json()["session_id"]
    session = get_session(session_id)
    assert session is not None
    for i, j in [[0, 0], [1, 0], [0, 1], [1, 1], [0, 2], [1, 2], [0, 3], [1, 3], [0, 4]]:
        session.board.put(i, j)

    response = client.post(f"/api/games/{session_id}/move", json={"position": [2, 2], "depth": 1})

    assert response.status_code == 400


def test_start_evicts_oldest_session_when_limit_is_reached():
    client = TestClient(app)
    first_session_id = client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1}).json()["session_id"]

    for _ in range(MAX_SESSIONS):
        client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1})

    assert first_session_id not in sessions
    assert len(sessions) == MAX_SESSIONS
