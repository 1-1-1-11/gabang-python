import json
from threading import RLock
from typing import Callable, Protocol, TypeVar
from uuid import uuid4

from backend.app.board import Board
from backend.app.game import GameSession
from backend.app.settings import DEFAULT_SESSION_TTL_SECONDS

T = TypeVar("T")


class RedisClient(Protocol):
    def set(self, name: str, value: str, ex: int | None = None) -> object: ...

    def get(self, name: str) -> bytes | str | None: ...

    def delete(self, *names: str) -> object: ...

    def keys(self, pattern: str) -> list[bytes | str]: ...


class RedisSessionStore:
    def __init__(self, client: RedisClient, ttl_seconds: int = DEFAULT_SESSION_TTL_SECONDS, key_prefix: str = "gobang:session:"):
        self.client = client
        self.ttl_seconds = ttl_seconds
        self.key_prefix = key_prefix
        self._lock = RLock()

    def create(self, session: GameSession) -> str:
        session_id = str(uuid4())
        self._save(session_id, session)
        return session_id

    def get(self, session_id: str) -> GameSession | None:
        raw = self.client.get(self._key(session_id))
        if raw is None:
            return None
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        return deserialize_session(json.loads(raw))

    def with_session(self, session_id: str, action: Callable[[GameSession], T], *, remove: bool = False) -> T | None:
        with self._lock:
            session = self.get(session_id)
            if session is None:
                return None
            result = action(session)
            if remove:
                self.client.delete(self._key(session_id))
            else:
                self._save(session_id, session)
            return result

    def remove(self, session_id: str) -> GameSession | None:
        session = self.get(session_id)
        self.client.delete(self._key(session_id))
        return session

    def clear(self) -> None:
        keys = self.client.keys(f"{self.key_prefix}*")
        if keys:
            self.client.delete(*[key.decode("utf-8") if isinstance(key, bytes) else key for key in keys])

    def prune_expired(self) -> None:
        return None

    def __contains__(self, session_id: object) -> bool:
        return isinstance(session_id, str) and self.get(session_id) is not None

    def __len__(self) -> int:
        return len(self.client.keys(f"{self.key_prefix}*"))

    def _save(self, session_id: str, session: GameSession) -> None:
        self.client.set(self._key(session_id), json.dumps(serialize_session(session)), ex=self.ttl_seconds)

    def _key(self, session_id: str) -> str:
        return f"{self.key_prefix}{session_id}"


def serialize_session(session: GameSession) -> dict:
    board = session.board
    return {
        "board": {
            "size": board.size,
            "first_role": board.first_role,
            "current_player": board.current_player,
            "history": [move.copy() for move in board.history],
        },
        "ai_first": session.ai_first,
        "depth": session.depth,
        "last_score": session.last_score,
        "last_best_path": [move.copy() for move in session.last_best_path],
        "last_current_depth": session.last_current_depth,
        "last_search_metrics": session.last_search_metrics.copy(),
    }


def deserialize_session(data: dict) -> GameSession:
    board_data = data["board"]
    board = Board(size=board_data["size"], first_role=board_data["first_role"])
    for move in board_data["history"]:
        board.put(move["i"], move["j"], move["role"])
    board.current_player = board_data["current_player"]
    return GameSession(
        board=board,
        ai_first=data["ai_first"],
        depth=data["depth"],
        last_score=data["last_score"],
        last_best_path=[move.copy() for move in data["last_best_path"]],
        last_current_depth=data["last_current_depth"],
        last_search_metrics=data.get("last_search_metrics", {}).copy(),
    )
