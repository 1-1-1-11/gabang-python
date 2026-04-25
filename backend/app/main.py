from fastapi import FastAPI

app = FastAPI(title="gobang-python")


@app.get("/api/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}
