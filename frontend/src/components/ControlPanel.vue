<script setup>
defineProps({
  isBusy: {
    type: Boolean,
    default: false,
  },
  hasSession: {
    type: Boolean,
    default: false,
  },
  canUndo: {
    type: Boolean,
    default: false,
  },
  canRestart: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["start-game", "undo-move", "end-game", "restart-game"]);
</script>

<template>
  <div class="panel-section control-panel" aria-label="游戏控制">
    <p class="section-label">Controls</p>
    <div class="button-row control-grid">
      <button
        id="start-button"
        type="button"
        :class="{ 'is-busy': isBusy }"
        :disabled="isBusy || hasSession"
        @click="emit('start-game')"
      >
        开始
      </button>
      <button
        id="undo-button"
        type="button"
        :class="{ 'is-busy': isBusy }"
        :disabled="isBusy || !hasSession || !canUndo"
        @click="emit('undo-move')"
      >
        悔棋
      </button>
      <button
        id="end-button"
        type="button"
        :class="{ 'is-busy': isBusy }"
        :disabled="isBusy || !hasSession"
        @click="emit('end-game')"
      >
        结束
      </button>
      <button
        id="restart-button"
        type="button"
        aria-label="重新开始"
        :class="{ 'is-busy': isBusy }"
        :disabled="isBusy || !canRestart"
        @click="emit('restart-game')"
      >
        重开
      </button>
    </div>
  </div>
</template>
