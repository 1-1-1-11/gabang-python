<script setup>
import AppLayout from "./components/AppLayout.vue";
import Board from "./components/Board.vue";
import ControlPanel from "./components/ControlPanel.vue";
import DifficultySelect from "./components/DifficultySelect.vue";
import ThinkingIndicator from "./components/ThinkingIndicator.vue";
import { useGameState } from "./composables/useGameState";

const props = defineProps({
  defaultApiBase: {
    type: String,
    default: "http://127.0.0.1:8000",
  },
});

const { state, boardStyle, startGame, playMove, undoMove, endGame, restartGame, cellDisabled, isLatest } = useGameState({
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
  <AppLayout>
    <template #eyebrow>
      gobang-python
    </template>

    <template #title>
      五子棋控制台
    </template>

    <template #status>
      <div id="status" class="status-pill" role="status">{{ state.status }}</div>
    </template>

    <template #board>
      <Board
        :board="state.board"
        :board-style="boardStyle"
        :cell-disabled="cellDisabled"
        :is-busy="state.isBusy"
        :is-latest="isLatest"
        :size="state.size"
        @play-move="playMove"
      />
    </template>

    <template #panel>
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
          <DifficultySelect
            v-model:depth="state.settings.depth"
            v-model:difficulty="state.settings.difficulty"
            :disabled="state.isBusy || Boolean(state.sessionId)"
          />
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

      <ControlPanel
        :can-restart="Boolean(state.sessionId) || state.history.length > 0 || Boolean(state.winner)"
        :can-undo="state.history.length > 0"
        :has-session="Boolean(state.sessionId)"
        :is-busy="state.isBusy"
        @end-game="endGame"
        @restart-game="restartGame"
        @start-game="startGame"
        @undo-move="undoMove"
      />

      <div class="panel-section">
        <p class="section-label">Thinking</p>
        <ThinkingIndicator :is-thinking="state.isBusy && state.status === 'AI 思考'" :metrics="state.searchMetrics" />
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
    </template>
  </AppLayout>
</template>
