import { createApp } from "vue";
import App from "./App.vue";
import "./styles.css";

const mountElement = document.querySelector("#app");

createApp(App, {
  defaultApiBase: mountElement?.dataset.apiBase ?? "http://127.0.0.1:8000",
}).mount(mountElement);
