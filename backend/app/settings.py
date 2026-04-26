import os


def get_cors_origins() -> list[str]:
    raw = os.getenv("GOBANG_CORS_ORIGINS", "*")
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return origins or ["*"]
