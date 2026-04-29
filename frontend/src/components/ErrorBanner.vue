<script setup>
defineProps({
  message: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["dismiss"]);
</script>

<template>
  <div v-if="message" id="error-banner" class="error-banner" role="alert">
    <span id="error-message">{{ message }}</span>
    <button id="error-dismiss-button" type="button" aria-label="关闭错误提示" @click="emit('dismiss')">
      关闭
    </button>
  </div>
</template>
