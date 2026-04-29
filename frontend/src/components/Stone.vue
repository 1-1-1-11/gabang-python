<script setup>
defineProps({
  role: {
    type: Number,
    required: true,
    validator: (value) => value === 1 || value === -1,
  },
  isLatest: {
    type: Boolean,
    default: false,
  },
});
</script>

<template>
  <span
    class="stone"
    :class="[role === 1 ? 'black' : 'white', { 'is-latest': isLatest }]"
    :aria-label="role === 1 ? '黑子' : '白子'"
    role="img"
  >
    <span v-if="isLatest" class="stone-latest-dot" aria-hidden="true"></span>
  </span>
</template>
