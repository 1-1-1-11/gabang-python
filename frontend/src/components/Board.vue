<script setup>
import Stone from "./Stone.vue";

defineProps({
  board: {
    type: Array,
    required: true,
  },
  size: {
    type: Number,
    required: true,
  },
  boardStyle: {
    type: Object,
    required: true,
  },
  isBusy: {
    type: Boolean,
    default: false,
  },
  cellDisabled: {
    type: Function,
    required: true,
  },
  isLatest: {
    type: Function,
    required: true,
  },
});

const emit = defineEmits(["play-move"]);

function roleName(role) {
  if (role === 1) {
    return "黑方";
  }
  if (role === -1) {
    return "白方";
  }
  return "空位";
}

function cellLabel(row, col, role, isLatestMove) {
  const label = `第 ${row + 1} 行，第 ${col + 1} 列，${roleName(role)}`;
  return isLatestMove ? `${label}，最后一步` : label;
}
</script>

<template>
  <div
    id="board"
    class="board"
    :class="{ 'is-busy': isBusy }"
    role="grid"
    :aria-label="`${size} x ${size} 五子棋棋盘`"
    :aria-busy="isBusy"
    :style="boardStyle"
  >
    <template v-for="(rowCells, row) in board" :key="row">
      <button
        v-for="(role, col) in rowCells"
        :key="`${row}-${col}`"
        class="cell"
        :class="{ 'is-latest': isLatest(row, col) }"
        type="button"
        role="gridcell"
        :aria-disabled="cellDisabled(row, col)"
        :aria-label="cellLabel(row, col, role, isLatest(row, col))"
        :data-row="row"
        :data-col="col"
        :disabled="cellDisabled(row, col)"
        @click="emit('play-move', row, col)"
      >
        <Stone v-if="role !== 0" :is-latest="isLatest(row, col)" :role="role" />
      </button>
    </template>
  </div>
</template>
