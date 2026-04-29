<script setup>
defineProps({
  winner: {
    type: Number,
    default: 0,
  },
  isGameOver: {
    type: Boolean,
    default: false,
  },
  isBusy: {
    type: Boolean,
    default: false,
  },
  canRestart: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["restart-game"]);

function resultLabel(winner) {
  if (winner === 1) {
    return "黑方胜";
  }
  if (winner === -1) {
    return "白方胜";
  }
  return "本局已结束";
}

function resultNote(winner) {
  if (winner === 1 || winner === -1) {
    return "胜负已定，棋盘已锁定。";
  }
  return "本局已结束，棋盘已锁定。";
}
</script>

<template>
  <section v-if="isGameOver" id="game-result" class="panel-section game-result" role="status" aria-live="polite">
    <p class="section-label">Result</p>
    <strong id="game-result-value">{{ resultLabel(winner) }}</strong>
    <p id="game-result-note">{{ resultNote(winner) }}</p>
    <button
      id="game-result-restart-button"
      type="button"
      :class="{ 'is-busy': isBusy }"
      :disabled="isBusy || !canRestart"
      @click="emit('restart-game')"
    >
      重新开始
    </button>
  </section>
</template>
