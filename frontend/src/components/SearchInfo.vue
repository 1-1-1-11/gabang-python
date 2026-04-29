<script setup>
defineProps({
  score: {
    type: Number,
    default: null,
  },
  currentDepth: {
    type: Number,
    default: null,
  },
  bestPath: {
    type: Array,
    default: () => [],
  },
  metrics: {
    type: Object,
    default: null,
  },
});

function metricValue(metrics, key) {
  return metrics?.[key] ?? "-";
}

function formatPath(path) {
  if (!path.length) {
    return "-";
  }
  return path.map(([row, col]) => `(${row + 1}, ${col + 1})`).join(" → ");
}
</script>

<template>
  <div class="panel-section search-info" aria-label="AI 搜索信息">
    <p class="section-label">Search</p>
    <div class="stats-grid search-stats">
      <div>
        <span>AI 评分</span>
        <strong id="ai-score-value">{{ score ?? "-" }}</strong>
      </div>
      <div>
        <span>搜索深度</span>
        <strong id="ai-depth-value">{{ currentDepth ?? "-" }}</strong>
      </div>
      <div>
        <span>节点</span>
        <strong id="search-nodes-value">{{ metricValue(metrics, "nodes") }}</strong>
      </div>
      <div>
        <span>截断</span>
        <strong id="search-beta-cutoffs-value">{{ metricValue(metrics, "beta_cutoffs") }}</strong>
      </div>
      <div>
        <span>缓存命中</span>
        <strong id="search-cache-hits-value">{{ metricValue(metrics, "cache_hits") }}</strong>
      </div>
      <div class="wide-stat">
        <span>主变路径</span>
        <strong id="best-path-value">{{ formatPath(bestPath) }}</strong>
      </div>
    </div>
  </div>
</template>
