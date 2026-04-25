from fastapi.testclient import TestClient

from backend.app.main import app


def test_openapi_documents_game_snapshot_and_best_path():
    client = TestClient(app)

    schema = client.get("/openapi.json").json()
    schemas = schema["components"]["schemas"]

    assert "GameSnapshot" in schemas
    assert "MoveRecord" in schemas
    assert schemas["GameSnapshot"]["properties"]["best_path"]["description"]
    assert "AI search principal variation" in schemas["GameSnapshot"]["properties"]["best_path"]["description"]


def test_game_endpoints_declare_success_and_error_models():
    client = TestClient(app)

    paths = client.get("/openapi.json").json()["paths"]

    start_responses = paths["/api/games/start"]["post"]["responses"]
    assert start_responses["200"]["content"]["application/json"]["schema"]["$ref"].endswith("/GameSnapshot")

    move_responses = paths["/api/games/{session_id}/move"]["post"]["responses"]
    assert move_responses["400"]["content"]["application/json"]["schema"]["$ref"].endswith("/ErrorResponse")
    assert move_responses["404"]["content"]["application/json"]["schema"]["$ref"].endswith("/ErrorResponse")

    undo_responses = paths["/api/games/{session_id}/undo"]["post"]["responses"]
    assert undo_responses["404"]["content"]["application/json"]["schema"]["$ref"].endswith("/ErrorResponse")

    end_responses = paths["/api/games/{session_id}/end"]["post"]["responses"]
    assert end_responses["404"]["content"]["application/json"]["schema"]["$ref"].endswith("/ErrorResponse")


def test_openapi_includes_request_examples():
    client = TestClient(app)

    paths = client.get("/openapi.json").json()["paths"]

    start_examples = paths["/api/games/start"]["post"]["requestBody"]["content"]["application/json"]["examples"]
    move_examples = paths["/api/games/{session_id}/move"]["post"]["requestBody"]["content"]["application/json"]["examples"]

    assert start_examples["human_first"]["value"] == {"size": 15, "ai_first": False, "depth": 4}
    assert move_examples["center_move"]["value"] == {"position": [7, 7], "depth": 4}
