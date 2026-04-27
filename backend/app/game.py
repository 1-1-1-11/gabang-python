from collections import OrderedDict
from dataclasses import dataclass, field
from threading import RLock
from time import monotonic
from typing import Callable, TypeVar
from uuid import uuid4

from backend.app.board import Board
from backend.app.minmax import minmax
from backend.app.settings import DEFAULT_MAX_SESSIONS, DEFAULT_SESSION_TTL_SECONDS, get_max_sessions, get_session_backend, get_session_ttl_seconds


@dataclass
class GameSession:
    board: Board
    ai_first: bool
    depth: int
    last_score: int = 0
    last_best_path: list[list[int]] = field(default_factory=list)
    last_current_depth: int = 0
    lock: RLock = field(default_factory=RLock, repr=False)


MAX_SESSIONS = DEFAULT_MAX_SESSIONS
SESSION_TTL_SECONDS = DEFAULT_SESSION_TTL_SECONDS
T = TypeVar("T")


class SessionStore:
    def __init__(self, max_sessions: int = MAX_SESSIONS, ttl_seconds: float = SESSION_TTL_SECONDS, clock: Callable[[], float] = monotonic):
        self.max_sessions = max_sessions
        self.ttl_seconds = ttl_seconds
        self._clock = clock
        self._items: OrderedDict[str, tuple[GameSession, float]] = OrderedDict()
        self._lock = RLock()

    def create(self, session: GameSession) -> str:
        with self._lock:
            self._prune_expired_locked()
            while len(self._items) >= self.max_sessions:
                self._items.popitem(last=False)
            session_id = str(uuid4())
            self._items[session_id] = (session, self._clock())
            return session_id

    def get(self, session_id: str) -> GameSession | None:
        with self._lock:
            return self._get_valid_locked(session_id)

    def with_session(self, session_id: str, action: Callable[[GameSession], T], *, remove: bool = False) -> T | None:
        with self._lock:
            session = self._get_valid_locked(session_id)
            if session is None:
                return None
            session.lock.acquire()
            if remove:
                self._items.pop(session_id, None)
        try:
            return action(session)
        finally:
            session.lock.release()

    def remove(self, session_id: str) -> GameSession | None:
        with self._lock:
            item = self._items.pop(session_id, None)
            return item[0] if item is not None else None

    def clear(self) -> None:
        with self._lock:
            self._items.clear()

    def prune_expired(self) -> None:
        with self._lock:
            self._prune_expired_locked()

    def __contains__(self, session_id: object) -> bool:
        return isinstance(session_id, str) and self.get(session_id) is not None

    def __len__(self) -> int:
        with self._lock:
            self._prune_expired_locked()
            return len(self._items)

    def _get_valid_locked(self, session_id: str) -> GameSession | None:
        item = self._items.get(session_id)
        if item is None:
            return None
        session, created_at = item
        if self._is_expired(created_at):
            self._items.pop(session_id, None)
            return None
        return session

    def _prune_expired_locked(self) -> None:
        expired = [session_id for session_id, (_, created_at) in self._items.items() if self._is_expired(created_at)]
        for session_id in expired:
            self._items.pop(session_id, None)

    def _is_expired(self, created_at: float) -> bool:
        return self._clock() - created_at >= self.ttl_seconds


def create_session_store() -> SessionStore:
    backend = get_session_backend()
    if backend == "redis":
        raise NotImplementedError("Redis session backend is not implemented yet.")
    return SessionStore(max_sessions=get_max_sessions(), ttl_seconds=get_session_ttl_seconds())


sessions = create_session_store()


def create_session(size: int, ai_first: bool, depth: int) -> tuple[str, GameSession]:
    session = GameSession(board=Board(size=size), ai_first=ai_first, depth=depth)
    session_id = sessions.create(session)
    if ai_first:
        with session.lock:
            play_ai_move(session, depth)
    return session_id, session


def get_session(session_id: str) -> GameSession | None:
    return sessions.get(session_id)


def with_session(session_id: str, action: Callable[[GameSession], T], *, remove: bool = False) -> T | None:
    return sessions.with_session(session_id, action, remove=remove)


def remove_session(session_id: str) -> GameSession | None:
    return sessions.remove(session_id)


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
