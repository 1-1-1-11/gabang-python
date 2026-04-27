import os


SESSION_BACKENDS = {"memory", "redis"}
DEFAULT_MAX_SESSIONS = 256
DEFAULT_SESSION_TTL_SECONDS = 60 * 60


def get_cors_origins() -> list[str]:
    raw = os.getenv("GOBANG_CORS_ORIGINS", "*")
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return origins or ["*"]


def get_session_backend() -> str:
    backend = os.getenv("GOBANG_SESSION_BACKEND", "memory").strip().lower()
    if backend not in SESSION_BACKENDS:
        raise ValueError("GOBANG_SESSION_BACKEND must be 'memory' or 'redis'.")
    return backend


def get_session_ttl_seconds() -> int:
    return _get_positive_int("GOBANG_SESSION_TTL_SECONDS", DEFAULT_SESSION_TTL_SECONDS)


def get_max_sessions() -> int:
    return _get_positive_int("GOBANG_MAX_SESSIONS", DEFAULT_MAX_SESSIONS)


def get_redis_url() -> str:
    return os.getenv("GOBANG_REDIS_URL", "redis://127.0.0.1:6379/0").strip()


def _get_positive_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be a positive integer.") from exc
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer.")
    return value
