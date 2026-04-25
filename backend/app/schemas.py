from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(description="Service health status.", examples=["ok"])


class StartGameRequest(BaseModel):
    size: int = Field(default=15, ge=5, le=25, description="Board size.")
    ai_first: bool = Field(default=False, description="Whether the AI places the first stone.")
    depth: int = Field(default=4, ge=1, le=8, description="Search depth for AI moves.")


class MoveRequest(BaseModel):
    position: tuple[int, int] = Field(description="Board coordinate as [row, column].")
    depth: int | None = Field(default=None, ge=1, le=8, description="Optional AI search depth override.")


class MoveRecord(BaseModel):
    i: int = Field(description="Move row index.")
    j: int = Field(description="Move column index.")
    role: int = Field(description="Player role for the move: 1 or -1.")


class GameSnapshot(BaseModel):
    session_id: str = Field(description="In-memory game session id.")
    board: list[list[int]] = Field(description="Board matrix using 0 for empty, 1 for first role, -1 for second role.")
    winner: int = Field(description="Winner role: 0 while undecided, otherwise 1 or -1.")
    current_player: int = Field(description="Role expected to move next.")
    history: list[MoveRecord] = Field(description="Ordered move history.")
    size: int = Field(description="Board size.")
    score: int = Field(description="Latest AI search score from the current perspective.")
    best_path: list[list[int]] = Field(description="AI search principal variation as a list of [row, column] moves.")
    current_depth: int = Field(description="Search depth used for the latest AI result.")


class ErrorResponse(BaseModel):
    detail: str = Field(description="Human-readable error message.")


GAME_ERROR_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Invalid game operation."},
    404: {"model": ErrorResponse, "description": "Game session not found."},
}
