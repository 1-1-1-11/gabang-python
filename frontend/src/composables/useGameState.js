import { computed, reactive } from "vue";

import { createGameApi, DEFAULT_API_BASE, normalizeApiBase } from "../api/client";

export const BOARD_SIZE = 15;
export const SEARCH_DEPTH = 4;
export const DEFAULT_DIFFICULTY = "normal";

export function emptyBoard(size) {
  return Array.from({ length: size }, () => Array(size).fill(0));
}

export function readApiBase(defaultApiBase = DEFAULT_API_BASE, search = window.location.search) {
  const params = new URLSearchParams(search);
  return normalizeApiBase(params.get("apiBase") || defaultApiBase, defaultApiBase);
}

export function useGameState(options = {}) {
  const defaultApiBase = options.defaultApiBase ?? DEFAULT_API_BASE;
  const gameApi = options.gameApi ?? createGameApi(readApiBase(defaultApiBase), defaultApiBase);

  const state = reactive({
    sessionId: null,
    board: emptyBoard(BOARD_SIZE),
    history: [],
    winner: 0,
    currentPlayer: 1,
    size: BOARD_SIZE,
    depth: SEARCH_DEPTH,
    score: null,
    bestPath: [],
    currentDepth: null,
    searchMetrics: null,
    errorMessage: "",
    isGameOver: false,
    isBusy: false,
    status: "待开始",
    settings: {
      size: BOARD_SIZE,
      depth: SEARCH_DEPTH,
      difficulty: DEFAULT_DIFFICULTY,
      apiBase: gameApi.apiBase,
      aiFirst: false,
    },
  });

  const latestMove = computed(() => state.history.at(-1) ?? null);
  const boardStyle = computed(() => ({ "--board-size": String(state.size) }));

  function setStatus(text) {
    state.status = text;
  }

  function setBusy(isBusy) {
    state.isBusy = isBusy;
  }

  function clearError() {
    state.errorMessage = "";
  }

  function setError(message) {
    state.errorMessage = message;
    setStatus(message);
  }

  function dismissError() {
    state.errorMessage = "";
  }

  function syncApiBase() {
    state.settings.apiBase = gameApi.setApiBase(state.settings.apiBase);
  }

  function applySnapshot(snapshot) {
    state.sessionId = snapshot.session_id;
    state.board = snapshot.board;
    state.history = snapshot.history;
    state.winner = snapshot.winner ?? 0;
    state.currentPlayer = snapshot.current_player;
    state.size = snapshot.size;
    state.depth = snapshot.current_depth || state.depth;
    state.score = snapshot.score;
    state.bestPath = snapshot.best_path ?? [];
    state.currentDepth = snapshot.current_depth;
    state.searchMetrics = snapshot.search_metrics ?? null;
    state.isGameOver = Boolean(state.winner);
  }

  async function startGame() {
    if (state.isBusy) {
      return;
    }
    setBusy(true);
    clearError();
    setStatus(state.settings.aiFirst ? "AI 思考" : "连接中");
    try {
      syncApiBase();
      const snapshot = await gameApi.startGame(state.settings);
      state.depth = Number(state.settings.depth);
      applySnapshot(snapshot);
      state.isGameOver = false;
      setStatus("进行中");
    } catch (error) {
      setError(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function playMove(row, col) {
    if (cellDisabled(row, col)) {
      return;
    }
    setBusy(true);
    clearError();
    setStatus("AI 思考");
    try {
      const snapshot = await gameApi.playMove(state.sessionId, [row, col], state.depth);
      applySnapshot(snapshot);
      setStatus(state.isGameOver ? "已结束" : "进行中");
    } catch (error) {
      setError(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function undoMove() {
    if (state.isBusy || !state.sessionId) {
      return;
    }
    setBusy(true);
    clearError();
    try {
      const snapshot = await gameApi.undoMove(state.sessionId);
      applySnapshot(snapshot);
      setStatus("已悔棋");
    } catch (error) {
      setError(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function endGame() {
    if (state.isBusy || !state.sessionId) {
      return;
    }
    setBusy(true);
    clearError();
    try {
      const snapshot = await gameApi.endGame(state.sessionId);
      applySnapshot(snapshot);
      state.sessionId = null;
      state.isGameOver = true;
      setStatus("已结束");
    } catch (error) {
      setError(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function restartGame() {
    if (state.isBusy || (!state.sessionId && state.history.length === 0 && !state.winner && !state.isGameOver)) {
      return;
    }
    setBusy(true);
    clearError();
    setStatus(state.sessionId ? "重开中" : "连接中");
    try {
      syncApiBase();
      if (state.sessionId) {
        const endedSnapshot = await gameApi.endGame(state.sessionId);
        applySnapshot(endedSnapshot);
        state.sessionId = null;
      }
      const snapshot = await gameApi.startGame(state.settings);
      state.depth = Number(state.settings.depth);
      applySnapshot(snapshot);
      state.isGameOver = false;
      setStatus("进行中");
    } catch (error) {
      setError(error.message);
    } finally {
      setBusy(false);
    }
  }

  function cellDisabled(row, col) {
    return state.isBusy || !state.sessionId || state.isGameOver || state.board[row]?.[col] !== 0;
  }

  function isLatest(row, col) {
    return latestMove.value?.i === row && latestMove.value?.j === col;
  }

  return {
    state,
    latestMove,
    boardStyle,
    setStatus,
    setBusy,
    clearError,
    setError,
    dismissError,
    syncApiBase,
    applySnapshot,
    startGame,
    playMove,
    undoMove,
    endGame,
    restartGame,
    cellDisabled,
    isLatest,
  };
}
