from typing import Annotated

from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware

from backend.app.game import create_session, play_ai_move, snapshot, with_session
from backend.app.schemas import GAME_ERROR_RESPONSES, GameSnapshot, HealthResponse, MoveRequest, StartGameRequest
from backend.app.settings import get_cors_origins

app = FastAPI(title="gobang-python")
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["system"], response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return service health status."""
    return HealthResponse(status="ok")


@app.post(
    "/api/games/start",
    tags=["games"],
    response_model=GameSnapshot,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "human_first": {"summary": "Human moves first", "value": {"size": 15, "ai_first": False, "depth": 4}},
                        "ai_first": {"summary": "AI moves first", "value": {"size": 15, "ai_first": True, "depth": 4}},
                    }
                }
            }
        }
    },
)
def start_game(request: StartGameRequest) -> GameSnapshot:
    """Create an in-memory game session."""
    session_id, session = create_session(request.size, request.ai_first, request.depth)
    return snapshot(session_id, session)


@app.post(
    "/api/games/{session_id}/move",
    tags=["games"],
    response_model=GameSnapshot,
    responses=GAME_ERROR_RESPONSES,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "center_move": {"summary": "Place a stone near center", "value": {"position": [7, 7], "depth": 4}}
                    }
                }
            }
        }
    },
)
def make_move(session_id: Annotated[str, Path(min_length=1)], request: MoveRequest) -> GameSnapshot:
    """Apply the player move and, if possible, an AI reply."""
    def apply_move(session):
        board = session.board
        if board.is_game_over():
            raise HTTPException(status_code=400, detail="Game is already over.")

        i, j = request.position
        if i >= board.size or j >= board.size:
            raise HTTPException(status_code=400, detail="Move position outside board.")
        if not board.put(i, j, board.current_player):
            raise HTTPException(status_code=400, detail="Invalid move.")

        if not board.is_game_over():
            play_ai_move(session, request.depth)
        return snapshot(session_id, session)

    response = with_session(session_id, apply_move)
    if response is None:
        raise HTTPException(status_code=404, detail="Game session not found.")
    return response


@app.post(
    "/api/games/{session_id}/undo",
    tags=["games"],
    response_model=GameSnapshot,
    responses={404: GAME_ERROR_RESPONSES[404]},
)
def undo_move(session_id: Annotated[str, Path(min_length=1)]) -> GameSnapshot:
    """Undo the latest player and AI moves when present."""
    def apply_undo(session):
        for _ in range(min(2, len(session.board.history))):
            session.board.undo()
        session.last_score = session.board.evaluate(session.board.current_player)
        session.last_best_path = []
        session.last_current_depth = 0
        return snapshot(session_id, session)

    response = with_session(session_id, apply_undo)
    if response is None:
        raise HTTPException(status_code=404, detail="Game session not found.")
    return response


@app.post(
    "/api/games/{session_id}/end",
    tags=["games"],
    response_model=GameSnapshot,
    responses={404: GAME_ERROR_RESPONSES[404]},
)
def end_game(session_id: Annotated[str, Path(min_length=1)]) -> GameSnapshot:
    """Return the final snapshot and remove the in-memory session."""
    response = with_session(session_id, lambda session: snapshot(session_id, session), remove=True)
    if response is None:
        raise HTTPException(status_code=404, detail="Game session not found.")
    return response
