<script setup>
import { computed } from "vue";

import AppLayout from "./components/AppLayout.vue";
import Board from "./components/Board.vue";
import ControlPanel from "./components/ControlPanel.vue";
import DifficultySelect from "./components/DifficultySelect.vue";
import ErrorBanner from "./components/ErrorBanner.vue";
import GameResult from "./components/GameResult.vue";
import MoveHistory from "./components/MoveHistory.vue";
import SearchInfo from "./components/SearchInfo.vue";
import ThinkingIndicator from "./components/ThinkingIndicator.vue";
import { useGameState } from "./composables/useGameState";

const props = defineProps({
  defaultApiBase: {
    type: String,
    default: "http://127.0.0.1:8000",
  },
});

const { state, boardStyle, startGame, playMove, undoMove, endGame, restartGame, dismissError, cellDisabled, isLatest } = useGameState({
  defaultApiBase: props.defaultApiBase,
});

const canRestart = computed(() => Boolean(state.sessionId) || state.history.length > 0 || Boolean(state.winner) || state.isGameOver);

function roleName(role) {
  if (role === 1) {
    return "黑方";
  }
  if (role === -1) {
    return "白方";
  }
  return "未定";
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
      <div id="status" class="status-pill" role="status" aria-live="polite">{{ state.status }}</div>
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
        :can-restart="canRestart"
        :can-undo="state.history.length > 0"
        :has-session="Boolean(state.sessionId)"
        :is-busy="state.isBusy"
        @end-game="endGame"
        @restart-game="restartGame"
        @start-game="startGame"
        @undo-move="undoMove"
      />

      <ErrorBanner :message="state.errorMessage" @dismiss="dismissError" />

      <GameResult
        :can-restart="canRestart"
        :is-busy="state.isBusy"
        :is-game-over="state.isGameOver"
        :winner="state.winner"
        @restart-game="restartGame"
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

      <SearchInfo
        :best-path="state.bestPath"
        :current-depth="state.currentDepth"
        :metrics="state.searchMetrics"
        :score="state.score"
      />

      <MoveHistory :moves="state.history" />
    </template>
  </AppLayout>
</template>
