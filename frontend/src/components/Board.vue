<script setup>
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
</script>

<template>
  <div
    id="board"
    class="board"
    :class="{ 'is-busy': isBusy }"
    role="grid"
    :aria-label="`${size} x ${size} 五子棋棋盘`"
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
        :aria-label="`row ${row + 1}, column ${col + 1}`"
        :data-row="row"
        :data-col="col"
        :disabled="cellDisabled(row, col)"
        @click="emit('play-move', row, col)"
      >
        <span v-if="role !== 0" class="stone" :class="role === 1 ? 'black' : 'white'" aria-hidden="true"></span>
      </button>
    </template>
  </div>
</template>
