from pydantic import BaseModel, Field, field_validator


class HealthResponse(BaseModel):
    status: str = Field(description="Service health status.", examples=["ok"])


class StartGameRequest(BaseModel):
    size: int = Field(default=15, ge=5, le=25, description="Board size.")
    ai_first: bool = Field(default=False, description="Whether the AI places the first stone.")
    depth: int = Field(default=4, ge=1, le=8, description="Search depth for AI moves.")


class MoveRequest(BaseModel):
    position: tuple[int, int] = Field(description="Board coordinate as [row, column].")
    depth: int | None = Field(default=None, ge=1, le=8, description="Optional AI search depth override.")

    @field_validator("position")
    @classmethod
    def position_must_be_non_negative(cls, position: tuple[int, int]) -> tuple[int, int]:
        if any(value < 0 for value in position):
            raise ValueError("position coordinates must be non-negative")
        return position


class MoveRecord(BaseModel):
    i: int = Field(description="Move row index.")
    j: int = Field(description="Move column index.")
    role: int = Field(description="Player role for the move: 1 or -1.")


class SearchMetricsSnapshot(BaseModel):
    nodes: int = Field(description="Search nodes visited by the latest AI search.")
    beta_cutoffs: int = Field(description="Alpha-beta beta-cutoff events from the latest AI search.")
    cache_hits: int = Field(description="Transposition cache hits from the latest AI search.")
    cache_stores: int = Field(description="Transposition cache stores from the latest AI search.")
    candidate_moves: int = Field(description="Candidate moves considered by the latest AI search.")
    leaf_nodes: int = Field(description="Leaf nodes evaluated by the latest AI search.")
    max_depth: int = Field(description="Maximum recursion depth reached by the latest AI search.")
    elapsed_ms: float = Field(description="Elapsed wall-clock time in milliseconds for the latest AI search.")


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
    search_metrics: SearchMetricsSnapshot = Field(description="Latest AI search metrics for frontend diagnostics.")


class ErrorResponse(BaseModel):
    detail: str = Field(description="Human-readable error message.")


GAME_ERROR_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Invalid game operation."},
    404: {"model": ErrorResponse, "description": "Game session not found."},
}
