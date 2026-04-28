<script setup>
import { useGameState } from "./composables/useGameState";

const props = defineProps({
  defaultApiBase: {
    type: String,
    default: "http://127.0.0.1:8000",
  },
});

const { state, boardStyle, startGame, playMove, undoMove, endGame, cellDisabled, isLatest } = useGameState({
  defaultApiBase: props.defaultApiBase,
});

function roleName(role) {
  if (role === 1) {
    return "黑方";
  }
  if (role === -1) {
    return "白方";
  }
  return "未定";
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
