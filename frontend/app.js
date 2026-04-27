const BOARD_SIZE = 15;
const SEARCH_DEPTH = 4;

const DEFAULT_API_BASE = document.body.dataset.apiBase ?? "http://127.0.0.1:8000";
const apiBaseInput = document.querySelector("#api-base-input");
apiBaseInput.value = readApiBase();
const boardElement = document.querySelector("#board");
const statusElement = document.querySelector("#status");
const moveListElement = document.querySelector("#move-list");
const startButton = document.querySelector("#start-button");
const undoButton = document.querySelector("#undo-button");
const endButton = document.querySelector("#end-button");
const boardSizeInput = document.querySelector("#board-size-input");
const searchDepthInput = document.querySelector("#search-depth-input");
const aiFirstInput = document.querySelector("#ai-first-input");
const sizeValue = document.querySelector("#size-value");
const depthValue = document.querySelector("#depth-value");
const currentPlayerValue = document.querySelector("#current-player-value");
const winnerValue = document.querySelector("#winner-value");
const aiScoreValue = document.querySelector("#ai-score-value");
const aiDepthValue = document.querySelector("#ai-depth-value");
const bestPathValue = document.querySelector("#best-path-value");

const state = {
  sessionId: null,
  board: Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(0)),
  history: [],
  winner: 0,
  currentPlayer: 1,
  size: BOARD_SIZE,
  depth: SEARCH_DEPTH,
  score: null,
  bestPath: [],
  currentDepth: null,
  isBusy: false,
  status: "待开始",
};

function roleName(role) {
  if (role === 1) {
    return "黑方";
  }
  if (role === -1) {
    return "白方";
  }
  return "未定";
}

function normalizeApiBase(candidate) {
  try {
    const url = new URL(candidate);
    if (url.protocol === "http:" || url.protocol === "https:") {
      return url.origin;
    }
  } catch {
    return DEFAULT_API_BASE;
  }
  return DEFAULT_API_BASE;
}

function readApiBase() {
  const params = new URLSearchParams(window.location.search);
  return normalizeApiBase(params.get("apiBase") || DEFAULT_API_BASE);
}

async function requestJson(path, options = {}) {
  apiBaseInput.value = normalizeApiBase(apiBaseInput.value);
  const response = await fetch(`${apiBaseInput.value}${path}`, {
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

function applySnapshot(snapshot) {
  state.sessionId = snapshot.session_id;
  state.board = snapshot.board;
  state.history = snapshot.history;
  state.winner = snapshot.winner;
  state.currentPlayer = snapshot.current_player;
  state.size = snapshot.size;
  state.depth = snapshot.current_depth || state.depth;
  state.score = snapshot.score;
  state.bestPath = snapshot.best_path ?? [];
  state.currentDepth = snapshot.current_depth;
  renderBoard();
  updateControls();
}

function readGameSettings() {
  return {
    size: Number(boardSizeInput.value),
    depth: Number(searchDepthInput.value),
    aiFirst: aiFirstInput.checked,
  };
}

async function startGame() {
  if (state.isBusy) {
    return;
  }
  const settings = readGameSettings();
  setBusy(true);
  setStatus("连接中");
  try {
    const snapshot = await requestJson("/api/games/start", {
      method: "POST",
      body: JSON.stringify({ size: settings.size, ai_first: settings.aiFirst, depth: settings.depth }),
    });
    state.depth = settings.depth;
    applySnapshot(snapshot);
    setStatus("进行中");
  } catch (error) {
    setStatus(error.message);
  } finally {
    setBusy(false);
  }
}

async function playMove(row, col) {
  if (state.isBusy || !state.sessionId || state.winner || state.board[row]?.[col] !== 0) {
    return;
  }
  setBusy(true);
  setStatus("AI 思考");
  try {
    const snapshot = await requestJson(`/api/games/${state.sessionId}/move`, {
      method: "POST",
      body: JSON.stringify({ position: [row, col], depth: state.depth }),
    });
    applySnapshot(snapshot);
    setStatus(snapshot.winner ? "已结束" : "进行中");
  } catch (error) {
    setStatus(error.message);
  } finally {
    setBusy(false);
  }
}

async function undoMove() {
  if (state.isBusy || !state.sessionId) {
    return;
  }
  setBusy(true);
  try {
    const snapshot = await requestJson(`/api/games/${state.sessionId}/undo`, { method: "POST" });
    applySnapshot(snapshot);
    setStatus("已悔棋");
  } catch (error) {
    setStatus(error.message);
  } finally {
    setBusy(false);
  }
}

async function endGame() {
  if (state.isBusy || !state.sessionId) {
    return;
  }
  setBusy(true);
  try {
    const snapshot = await requestJson(`/api/games/${state.sessionId}/end`, { method: "POST" });
    applySnapshot(snapshot);
    state.sessionId = null;
    setStatus("已结束");
  } catch (error) {
    setStatus(error.message);
  } finally {
    setBusy(false);
  }
}

function setStatus(text) {
  state.status = text;
  statusElement.textContent = text;
}

function setBusy(isBusy) {
  state.isBusy = isBusy;
  startButton.classList.toggle("is-busy", isBusy);
  undoButton.classList.toggle("is-busy", isBusy);
  endButton.classList.toggle("is-busy", isBusy);
  boardElement.classList.toggle("is-busy", isBusy);
  updateControls();
}

function updateControls() {
  startButton.disabled = state.isBusy || Boolean(state.sessionId);
  undoButton.disabled = state.isBusy || !state.sessionId || state.history.length === 0;
  endButton.disabled = state.isBusy || !state.sessionId;
  boardSizeInput.disabled = state.isBusy || Boolean(state.sessionId);
  searchDepthInput.disabled = state.isBusy || Boolean(state.sessionId);
  apiBaseInput.disabled = state.isBusy || Boolean(state.sessionId);
  aiFirstInput.disabled = state.isBusy || Boolean(state.sessionId);

  for (const cell of boardElement.querySelectorAll(".cell")) {
    const row = Number(cell.dataset.row);
    const col = Number(cell.dataset.col);
    cell.disabled = state.isBusy || !state.sessionId || Boolean(state.winner) || state.board[row]?.[col] !== 0;
  }
}

function latestMove() {
  return state.history.at(-1) ?? null;
}

function createCell(row, col) {
  const cell = document.createElement("button");
  cell.className = "cell";
  const latest = latestMove();
  if (latest?.i === row && latest?.j === col) {
    cell.classList.add("is-latest");
  }
  cell.type = "button";
  cell.setAttribute("role", "gridcell");
  cell.setAttribute("aria-label", `row ${row + 1}, column ${col + 1}`);
  cell.dataset.row = String(row);
  cell.dataset.col = String(col);
  cell.disabled = state.isBusy || !state.sessionId || Boolean(state.winner) || state.board[row]?.[col] !== 0;
  cell.addEventListener("click", () => {
    playMove(row, col);
  });
  return cell;
}

function placeStone(cell, role) {
  const stone = document.createElement("span");
  stone.className = `stone ${role === 1 ? "black" : "white"}`;
  stone.setAttribute("aria-hidden", "true");
  cell.append(stone);
}

function renderMoveList() {
  moveListElement.replaceChildren(
    ...state.history.map((move, index) => {
      const item = document.createElement("li");
      if (index === state.history.length - 1) {
        item.className = "is-latest";
      }
      item.textContent = `${index + 1}. ${roleName(move.role)} (${move.i + 1}, ${move.j + 1})`;
      return item;
    }),
  );
}

function formatPath(path) {
  if (!path.length) {
    return "-";
  }
  return path.map(([row, col]) => `(${row + 1}, ${col + 1})`).join(" → ");
}

function renderStats() {
  sizeValue.textContent = `${state.size} x ${state.size}`;
  depthValue.textContent = String(state.depth);
  currentPlayerValue.textContent = roleName(state.currentPlayer);
  winnerValue.textContent = roleName(state.winner);
  aiScoreValue.textContent = state.score ?? "-";
  aiDepthValue.textContent = state.currentDepth ?? "-";
  bestPathValue.textContent = formatPath(state.bestPath);
}

function renderBoard() {
  document.documentElement.style.setProperty("--board-size", String(state.size));
  const cells = [];

  for (let row = 0; row < state.size; row += 1) {
    for (let col = 0; col < state.size; col += 1) {
      const cell = createCell(row, col);
      const role = state.board[row][col];
      if (role !== 0) {
        placeStone(cell, role);
      }
      cells.push(cell);
    }
  }

  boardElement.replaceChildren(...cells);
  renderStats();
  renderMoveList();
}

startButton.addEventListener("click", () => {
  startGame();
});

undoButton.addEventListener("click", () => {
  undoMove();
});

endButton.addEventListener("click", () => {
  endGame();
});

setStatus("待开始");
renderBoard();
updateControls();
