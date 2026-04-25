from typing import Annotated

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field

from backend.app.game import create_session, get_session, play_ai_move, remove_session, snapshot

app = FastAPI(title="gobang-python")


class StartGameRequest(BaseModel):
    size: int = Field(default=15, ge=5, le=25)
    ai_first: bool = False
    depth: int = Field(default=4, ge=1, le=8)


class MoveRequest(BaseModel):
    position: tuple[int, int]
    depth: int | None = Field(default=None, ge=1, le=8)


@app.get("/api/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}


@app.post("/api/games/start", tags=["games"])
def start_game(request: StartGameRequest) -> dict:
    """Create an in-memory game session."""
    session_id, session = create_session(request.size, request.ai_first, request.depth)
    return snapshot(session_id, session)


@app.post("/api/games/{session_id}/move", tags=["games"])
def make_move(session_id: Annotated[str, Path(min_length=1)], request: MoveRequest) -> dict:
    """Apply the player move and, if possible, an AI reply."""
    session = get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game session not found.")

    i, j = request.position
    board = session.board
    if not board.put(i, j, board.current_player):
        raise HTTPException(status_code=400, detail="Invalid move.")

    if not board.is_game_over():
        play_ai_move(session, request.depth)
    return snapshot(session_id, session)


@app.post("/api/games/{session_id}/undo", tags=["games"])
def undo_move(session_id: Annotated[str, Path(min_length=1)]) -> dict:
    """Undo the latest player and AI moves when present."""
    session = get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game session not found.")

    session.board.undo()
    session.board.undo()
    session.last_score = session.board.evaluate(session.board.current_player)
    session.last_best_path = []
    session.last_current_depth = 0
    return snapshot(session_id, session)


@app.post("/api/games/{session_id}/end", tags=["games"])
def end_game(session_id: Annotated[str, Path(min_length=1)]) -> dict:
    """Return the final snapshot and remove the in-memory session."""
    session = remove_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Game session not found.")
    return snapshot(session_id, session)
