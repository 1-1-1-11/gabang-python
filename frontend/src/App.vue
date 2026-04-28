<script setup>
import { computed, reactive } from "vue";

const props = defineProps({
  defaultApiBase: {
    type: String,
    default: "http://127.0.0.1:8000",
  },
});

const BOARD_SIZE = 15;
const SEARCH_DEPTH = 4;

function emptyBoard(size) {
  return Array.from({ length: size }, () => Array(size).fill(0));
}

function normalizeApiBase(candidate) {
  try {
    const url = new URL(candidate);
    if (url.protocol === "http:" || url.protocol === "https:") {
      return url.origin;
    }
  } catch {
    return props.defaultApiBase;
  }
  return props.defaultApiBase;
}

function readApiBase() {
  const params = new URLSearchParams(window.location.search);
  return normalizeApiBase(params.get("apiBase") || props.defaultApiBase);
}

const state = reactive({
  sessionId: null,
  board: emptyBoard(BOARD_SIZE),
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
  settings: {
    size: BOARD_SIZE,
    depth: SEARCH_DEPTH,
    apiBase: readApiBase(),
    aiFirst: false,
  },
});

const latestMove = computed(() => state.history.at(-1) ?? null);
const boardStyle = computed(() => ({ "--board-size": String(state.size) }));

function roleName(role) {
  if (role === 1) {
    return "黑方";
  }
  if (role === -1) {
    return "白方";
  }
  return "未定";
}

function setStatus(text) {
  state.status = text;
}

function setBusy(isBusy) {
  state.isBusy = isBusy;
}

async function requestJson(path, options = {}) {
  state.settings.apiBase = normalizeApiBase(state.settings.apiBase);
  const response = await fetch(`${state.settings.apiBase}${path}`, {
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
      body: JSON.stringify({
        size: Number(state.settings.size),
        ai_first: state.settings.aiFirst,
        depth: Number(state.settings.depth),
      }),
    });
    state.depth = Number(state.settings.depth);
    applySnapshot(snapshot);
    setStatus("进行中");
  } catch (error) {
    setStatus(error.message);
  } finally {
    setBusy(false);
  }
}

async function playMove(row, col) {
  if (cellDisabled(row, col)) {
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

function cellDisabled(row, col) {
  return state.isBusy || !state.sessionId || Boolean(state.winner) || state.board[row]?.[col] !== 0;
}

function isLatest(row, col) {
  return latestMove.value?.i === row && latestMove.value?.j === col;
}

function formatPath(path) {
  if (!path.length) {
    return "-";
  }
  return path.map(([row, col]) => `(${row + 1}, ${col + 1})`).join(" → ");
}
</script>

<template>
  <main class="app-shell" aria-label="gobang-python">
    <section class="play-surface" aria-label="棋局">
      <header class="topbar">
        <div>
          <p class="eyebrow">gobang-python</p>
          <h1>五子棋控制台</h1>
        </div>
        <div id="status" class="status-pill" role="status">{{ state.status }}</div>
      </header>

      <div class="board-zone">
        <div
          id="board"
          class="board"
          :class="{ 'is-busy': state.isBusy }"
          role="grid"
          :aria-label="`${state.size} x ${state.size} 五子棋棋盘`"
          :style="boardStyle"
        >
          <template v-for="(rowCells, row) in state.board" :key="row">
            <button
              v-for="(role, col) in rowCells"
              :key="`${row}-${col}`"
              class="cell"
              :class="{ 'is-latest': isLatest(row, col) }"
              type="button"
              role="gridcell"
              :aria-label="`row ${row + 1}, column ${col + 1}`"
              :data-row="row"
              :data-col="col"
              :disabled="cellDisabled(row, col)"
              @click="playMove(row, col)"
            >
              <span v-if="role !== 0" class="stone" :class="role === 1 ? 'black' : 'white'" aria-hidden="true"></span>
            </button>
          </template>
        </div>
      </div>
    </section>

    <aside class="side-panel" aria-label="棋局控制">
      <div class="panel-section">
        <p class="section-label">Settings</p>
        <div class="settings-grid">
          <label for="board-size-input">
            棋盘
            <input
              id="board-size-input"
              v-model.number="state.settings.size"
              type="number"
              min="5"
              max="25"
              aria-describedby="board-size-hint"
              :disabled="state.isBusy || Boolean(state.sessionId)"
            >
            <span id="board-size-hint" class="field-hint">范围 5-25，演示推荐 6-15。</span>
          </label>
          <label for="search-depth-input">
            深度
            <input
              id="search-depth-input"
              v-model.number="state.settings.depth"
              type="number"
              min="1"
              max="8"
              aria-describedby="search-depth-hint"
              :disabled="state.isBusy || Boolean(state.sessionId)"
            >
            <span id="search-depth-hint" class="field-hint">范围 1-8，深度越高 AI 思考越慢。</span>
          </label>
          <label for="api-base-input">
            API 地址
            <input
              id="api-base-input"
              v-model="state.settings.apiBase"
              type="url"
              aria-describedby="api-base-hint"
              :disabled="state.isBusy || Boolean(state.sessionId)"
            >
            <span id="api-base-hint" class="field-hint">可用 ?apiBase= 覆盖，仅支持 http(s)。</span>
          </label>
          <label class="checkbox-row" for="ai-first-input">
            <input
              id="ai-first-input"
              v-model="state.settings.aiFirst"
              type="checkbox"
              :disabled="state.isBusy || Boolean(state.sessionId)"
            >
            AI 先手
          </label>
        </div>
      </div>

      <div class="panel-section">
        <p class="section-label">Controls</p>
        <div class="button-row">
          <button
            id="start-button"
            type="button"
            :class="{ 'is-busy': state.isBusy }"
            :disabled="state.isBusy || Boolean(state.sessionId)"
            @click="startGame"
          >
            开始
          </button>
          <button
            id="undo-button"
            type="button"
            :class="{ 'is-busy': state.isBusy }"
            :disabled="state.isBusy || !state.sessionId || state.history.length === 0"
            @click="undoMove"
          >
            悔棋
          </button>
          <button
            id="end-button"
            type="button"
            :class="{ 'is-busy': state.isBusy }"
            :disabled="state.isBusy || !state.sessionId"
            @click="endGame"
          >
            结束
          </button>
        </div>
      </div>

      <div class="panel-section stats-grid" aria-label="棋局状态">
        <div>
          <span>棋盘</span>
          <strong id="size-value">{{ state.size }} x {{ state.size }}</strong>
        </div>
        <div>
          <span>深度</span>
          <strong id="depth-value">{{ state.depth }}</strong>
        </div>
        <div>
          <span>当前</span>
          <strong id="current-player-value">{{ roleName(state.currentPlayer) }}</strong>
        </div>
        <div>
          <span>胜者</span>
          <strong id="winner-value">{{ roleName(state.winner) }}</strong>
        </div>
      </div>

      <div class="panel-section stats-grid" aria-label="AI 搜索信息">
        <div>
          <span>AI 评分</span>
          <strong id="ai-score-value">{{ state.score ?? "-" }}</strong>
        </div>
        <div>
          <span>搜索深度</span>
          <strong id="ai-depth-value">{{ state.currentDepth ?? "-" }}</strong>
        </div>
        <div class="wide-stat">
          <span>主变路径</span>
          <strong id="best-path-value">{{ formatPath(state.bestPath) }}</strong>
        </div>
      </div>

      <div class="panel-section">
        <p class="section-label">Moves</p>
        <ol id="move-list" class="move-list" aria-label="落子记录">
          <li
            v-for="(move, index) in state.history"
            :key="`${index}-${move.i}-${move.j}`"
            :class="{ 'is-latest': index === state.history.length - 1 }"
          >
            {{ index + 1 }}. {{ roleName(move.role) }} ({{ move.i + 1 }}, {{ move.j + 1 }})
          </li>
        </ol>
      </div>
    </aside>
  </main>
</template>
