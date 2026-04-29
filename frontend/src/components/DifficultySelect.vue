<script setup>
const DIFFICULTY_LEVELS = [
  { id: "easy", label: "简单", depth: 2 },
  { id: "normal", label: "普通", depth: 4 },
  { id: "hard", label: "困难", depth: 6 },
  { id: "custom", label: "自定义", depth: null },
];

const difficulty = defineModel("difficulty", {
  type: String,
  default: "normal",
});

const depth = defineModel("depth", {
  type: Number,
  default: 4,
});

defineProps({
  disabled: {
    type: Boolean,
    default: false,
  },
});

function selectDifficulty(level) {
  difficulty.value = level.id;
  if (level.depth !== null) {
    depth.value = level.depth;
  }
}
</script>

<template>
  <div class="difficulty-field">
    <span class="field-label">难度</span>
    <div class="difficulty-options" role="group" aria-label="难度选择">
      <button
        v-for="level in DIFFICULTY_LEVELS"
        :id="`difficulty-${level.id}`"
        :key="level.id"
        type="button"
        class="difficulty-option"
        :aria-pressed="difficulty === level.id"
        :class="{ 'is-active': difficulty === level.id }"
        :disabled="disabled"
        @click="selectDifficulty(level)"
      >
        <span>{{ level.label }}</span>
        <strong>{{ level.depth === null ? `${depth} 层` : `${level.depth} 层` }}</strong>
      </button>
    </div>
    <label v-if="difficulty === 'custom'" class="custom-depth-field" for="search-depth-input">
      自定义深度
      <input
        id="search-depth-input"
        v-model.number="depth"
        type="number"
        min="1"
        max="8"
        aria-describedby="search-depth-hint"
        :disabled="disabled"
      >
    </label>
    <span id="search-depth-hint" class="field-hint">简单/普通/困难分别映射到现有 depth 2/4/6；自定义范围 1-8。</span>
  </div>
</template>
