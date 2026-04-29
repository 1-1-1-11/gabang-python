<script setup>
defineProps({
  isThinking: {
    type: Boolean,
    default: false,
  },
  metrics: {
    type: Object,
    default: null,
  },
});

function metricValue(metrics, key) {
  return metrics?.[key] ?? "-";
}

function elapsedValue(metrics) {
  const elapsed = metrics?.elapsed_ms;
  if (elapsed === null || elapsed === undefined) {
    return "-";
  }
  return `${Number(elapsed).toFixed(1)} ms`;
}
</script>

<template>
  <div id="thinking-indicator" class="thinking-indicator" :class="{ 'is-thinking': isThinking }" aria-live="polite">
    <div class="thinking-header">
      <span class="thinking-dot" aria-hidden="true"></span>
      <strong id="thinking-state-value">{{ isThinking ? "AI 思考中" : "AI 待命" }}</strong>
    </div>
    <dl class="thinking-metrics" aria-label="AI 思考指标">
      <div>
        <dt>耗时</dt>
        <dd id="thinking-elapsed-value">{{ elapsedValue(metrics) }}</dd>
      </div>
      <div>
        <dt>节点</dt>
        <dd id="thinking-nodes-value">{{ metricValue(metrics, "nodes") }}</dd>
      </div>
      <div>
        <dt>截断</dt>
        <dd id="thinking-beta-cutoffs-value">{{ metricValue(metrics, "beta_cutoffs") }}</dd>
      </div>
    </dl>
  </div>
</template>
