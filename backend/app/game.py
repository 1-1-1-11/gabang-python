from dataclasses import dataclass, field
from uuid import uuid4

from backend.app.board import Board
from backend.app.minmax import minmax


@dataclass
class GameSession:
    board: Board
    ai_first: bool
    depth: int
    last_score: int = 0
    last_best_path: list[list[int]] = field(default_factory=list)
    last_current_depth: int = 0


MAX_SESSIONS = 256
sessions: dict[str, GameSession] = {}


def create_session(size: int, ai_first: bool, depth: int) -> tuple[str, GameSession]:
    if len(sessions) >= MAX_SESSIONS:
        sessions.pop(next(iter(sessions)))

    session_id = str(uuid4())
    session = GameSession(board=Board(size=size), ai_first=ai_first, depth=depth)
    sessions[session_id] = session
    if ai_first:
        play_ai_move(session, depth)
    return session_id, session


def get_session(session_id: str) -> GameSession | None:
    return sessions.get(session_id)


def remove_session(session_id: str) -> GameSession | None:
    return sessions.pop(session_id, None)


def play_ai_move(session: GameSession, depth: int | None = None) -> bool:
    board = session.board
    if board.is_game_over():
        session.last_score = board.evaluate(board.current_player)
        session.last_best_path = []
        session.last_current_depth = 0
        return False

    search_depth = depth or session.depth
    score, move, path = minmax(board, board.current_player, depth=search_depth)
    session.last_score = score
    session.last_best_path = path
    session.last_current_depth = search_depth

    if move is None:
        return False
    return board.put(move[0], move[1], board.current_player)


def snapshot(session_id: str, session: GameSession) -> dict:
    board = session.board
    return {
        "session_id": session_id,
        "board": [row.copy() for row in board.board],
        "winner": board.get_winner(),
        "current_player": board.current_player,
        "history": [move.copy() for move in board.history],
        "size": board.size,
        "score": session.last_score,
        "best_path": session.last_best_path or [],
        "current_depth": session.last_current_depth,
    }
