const BOARD_SIZE = 15;
const SEARCH_DEPTH = 4;

const apiBase = document.body.dataset.apiBase ?? "http://127.0.0.1:8000";
const boardElement = document.querySelector("#board");
const statusElement = document.querySelector("#status");
const moveListElement = document.querySelector("#move-list");
const startButton = document.querySelector("#start-button");
const undoButton = document.querySelector("#undo-button");
const endButton = document.querySelector("#end-button");
const sizeValue = document.querySelector("#size-value");
const depthValue = document.querySelector("#depth-value");
const currentPlayerValue = document.querySelector("#current-player-value");
const winnerValue = document.querySelector("#winner-value");

const state = {
  sessionId: null,
  board: Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(0)),
  history: [],
  winner: 0,
  currentPlayer: 1,
  size: BOARD_SIZE,
  depth: SEARCH_DEPTH,
  isBusy: false,
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

async function requestJson(path, options = {}) {
  const response = await fetch(`${apiBase}${path}`, {
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
  renderBoard();
}

async function startGame() {
  if (state.isBusy) {
    return;
  }
  setBusy(true);
  setStatus("连接中");
  try {
    const snapshot = await requestJson("/api/games/start", {
      method: "POST",
      body: JSON.stringify({ size: BOARD_SIZE, ai_first: false, depth: SEARCH_DEPTH }),
    });
    applySnapshot(snapshot);
    setStatus("进行中");
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
      body: JSON.stringify({ position: [row, col], depth: SEARCH_DEPTH }),
    });
    applySnapshot(snapshot);
    setStatus(snapshot.winner ? "已结束" : "进行中");
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
  } finally {
    setBusy(false);
  }
}

function setStatus(text) {
  statusElement.textContent = text;
}

function setBusy(isBusy) {
  state.isBusy = isBusy;
  startButton.disabled = isBusy;
  undoButton.disabled = isBusy;
  endButton.disabled = isBusy;
  boardElement.classList.toggle("is-busy", isBusy);
}

function createCell(row, col) {
  const cell = document.createElement("button");
  cell.className = "cell";
  cell.type = "button";
  cell.setAttribute("role", "gridcell");
  cell.setAttribute("aria-label", `row ${row + 1}, column ${col + 1}`);
  cell.dataset.row = String(row);
  cell.dataset.col = String(col);
  cell.disabled = state.isBusy;
  cell.addEventListener("click", () => {
    playMove(row, col).catch((error) => setStatus(error.message));
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
      item.textContent = `${index + 1}. ${roleName(move.role)} (${move.i}, ${move.j})`;
      return item;
    }),
  );
}

function renderStats() {
  sizeValue.textContent = `${state.size} x ${state.size}`;
  depthValue.textContent = String(state.depth);
  currentPlayerValue.textContent = roleName(state.currentPlayer);
  winnerValue.textContent = roleName(state.winner);
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
  startGame().catch((error) => setStatus(error.message));
});

undoButton.addEventListener("click", () => {
  undoMove().catch((error) => setStatus(error.message));
});

endButton.addEventListener("click", () => {
  endGame().catch((error) => setStatus(error.message));
});

setStatus("待开始");
renderBoard();
