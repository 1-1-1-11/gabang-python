const { defineConfig } = require("vite");
const vue = require("@vitejs/plugin-vue");

module.exports = defineConfig({
  root: "frontend",
  plugins: [vue()],
  build: {
    outDir: "../dist/frontend",
    emptyOutDir: true,
  },
  server: {
    host: "127.0.0.1",
    port: 4173,
  },
  preview: {
    host: "127.0.0.1",
    port: 4173,
  },
});
