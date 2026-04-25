from fastapi.testclient import TestClient

from backend.app.main import app


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


def test_end_releases_game_session():
    client = TestClient(app)
    session_id = client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1}).json()["session_id"]

    response = client.post(f"/api/games/{session_id}/end")

    assert response.status_code == 200
    assert response.json()["session_id"] == session_id
    assert client.post(f"/api/games/{session_id}/undo").status_code == 404


def test_move_rejects_unknown_session_and_occupied_position():
    client = TestClient(app)

    missing = client.post("/api/games/not-found/move", json={"position": [2, 2], "depth": 1})
    assert missing.status_code == 404

    session_id = client.post("/api/games/start", json={"size": 6, "ai_first": False, "depth": 1}).json()["session_id"]
    client.post(f"/api/games/{session_id}/move", json={"position": [2, 2], "depth": 1})
    occupied = client.post(f"/api/games/{session_id}/move", json={"position": [2, 2], "depth": 1})

    assert occupied.status_code == 400
