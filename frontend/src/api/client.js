export const DEFAULT_API_BASE = "http://127.0.0.1:8000";

export function normalizeApiBase(candidate, fallback = DEFAULT_API_BASE) {
  try {
    const url = new URL(candidate);
    if (url.protocol === "http:" || url.protocol === "https:") {
      return url.origin;
    }
  } catch {
    return fallback;
  }
  return fallback;
}

export function createGameApi(apiBase, fallbackApiBase = DEFAULT_API_BASE) {
  let base = normalizeApiBase(apiBase, fallbackApiBase);

  async function requestJson(path, options = {}) {
    const response = await fetch(`${base}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
    const text = await response.text();
    let payload;
    try {
      payload = text ? JSON.parse(text) : {};
    } catch {
      throw new Error("响应格式错误");
    }
    if (!response.ok) {
      throw new Error(payload.detail ?? "请求失败");
    }
    return payload;
  }

  return {
    get apiBase() {
      return base;
    },
    setApiBase(candidate) {
      base = normalizeApiBase(candidate, fallbackApiBase);
      return base;
    },
    health() {
      return requestJson("/api/health");
    },
    startGame(settings) {
      return requestJson("/api/games/start", {
        method: "POST",
        body: JSON.stringify({
          size: Number(settings.size),
          ai_first: Boolean(settings.aiFirst),
          depth: Number(settings.depth),
        }),
      });
    },
    playMove(sessionId, position, depth) {
      return requestJson(`/api/games/${sessionId}/move`, {
        method: "POST",
        body: JSON.stringify({ position, depth }),
      });
    },
    undoMove(sessionId) {
      return requestJson(`/api/games/${sessionId}/undo`, { method: "POST" });
    },
    endGame(sessionId) {
      return requestJson(`/api/games/${sessionId}/end`, { method: "POST" });
    },
  };
}
