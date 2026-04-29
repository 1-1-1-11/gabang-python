<script setup>
defineProps({
  moves: {
    type: Array,
    required: true,
  },
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
</script>

<template>
  <div class="panel-section move-history">
    <p class="section-label">Moves</p>
    <p v-if="moves.length === 0" id="move-empty" class="move-empty">暂无落子</p>
    <ol id="move-list" class="move-list" aria-label="落子记录">
      <li
        v-for="(move, index) in moves"
        :key="`${index}-${move.i}-${move.j}`"
        :class="{ 'is-latest': index === moves.length - 1 }"
      >
        <span class="move-index">{{ index + 1 }}.</span>
        <span class="move-role">{{ roleName(move.role) }}</span>
        <span class="move-position"> ({{ move.i + 1 }}, {{ move.j + 1 }})</span>
      </li>
    </ol>
  </div>
</template>
