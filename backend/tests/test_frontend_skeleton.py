from html.parser import HTMLParser
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"
FRONTEND_SRC = FRONTEND / "src"
E2E_SPEC = ROOT / "e2e" / "gobang.spec.js"
API_CLIENT = FRONTEND_SRC / "api" / "client.js"
GAME_STATE = FRONTEND_SRC / "composables" / "useGameState.js"
APP_LAYOUT = FRONTEND_SRC / "components" / "AppLayout.vue"
THEME_CSS = FRONTEND_SRC / "theme.css"
BOARD_COMPONENT = FRONTEND_SRC / "components" / "Board.vue"
STONE_COMPONENT = FRONTEND_SRC / "components" / "Stone.vue"
CONTROL_PANEL_COMPONENT = FRONTEND_SRC / "components" / "ControlPanel.vue"
DIFFICULTY_SELECT_COMPONENT = FRONTEND_SRC / "components" / "DifficultySelect.vue"
THINKING_INDICATOR_COMPONENT = FRONTEND_SRC / "components" / "ThinkingIndicator.vue"
MOVE_HISTORY_COMPONENT = FRONTEND_SRC / "components" / "MoveHistory.vue"
SEARCH_INFO_COMPONENT = FRONTEND_SRC / "components" / "SearchInfo.vue"
ERROR_BANNER_COMPONENT = FRONTEND_SRC / "components" / "ErrorBanner.vue"
GAME_RESULT_COMPONENT = FRONTEND_SRC / "components" / "GameResult.vue"


class ElementCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def parse_index() -> ElementCollector:
    parser = ElementCollector()
    parser.feed((FRONTEND / "index.html").read_text(encoding="utf-8"))
    return parser


def test_frontend_uses_new_static_directory_only():
    forbidden_paths = [
        ROOT / "src",
        ROOT / "public",
        ROOT / "images",
        ROOT / "config-overrides.js",
        ROOT / "vue.config.js",
        ROOT / ".eslintignore",
    ]

    assert FRONTEND.is_dir()
    assert all(not path.exists() for path in forbidden_paths)


def test_node_tooling_runs_vue_vite_frontend():
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    playwright_config = (ROOT / "playwright.config.js").read_text(encoding="utf-8")
    vite_config = (ROOT / "vite.config.js").read_text(encoding="utf-8")
    scripts = package.get("scripts", {})
    dependencies = package.get("dependencies", {})
    dev_dependencies = package.get("devDependencies", {})
    lockfile = (ROOT / "package-lock.json").read_text(encoding="utf-8")

    assert scripts["dev:frontend"] == "vite"
    assert scripts["build"] == "vite build"
    assert scripts["preview:frontend"] == "vite preview"
    assert scripts["test:e2e"] == "playwright test"
    assert scripts["test:e2e:headed"] == "playwright test --headed"
    assert 'baseURL: "http://127.0.0.1:5173"' in playwright_config
    assert "npm run dev:frontend -- --host 127.0.0.1 --port 5173" in playwright_config
    assert "port: 5173" in vite_config
    assert set(dependencies) == {"vue"}
    assert {"@playwright/test", "@vitejs/plugin-vue", "vite"}.issubset(dev_dependencies)
    for forbidden in ("react", "react-dom", "webpack", "config-overrides"):
        assert forbidden not in dependencies
        assert forbidden not in dev_dependencies
        assert f'node_modules/{forbidden}' not in lockfile


def test_frontend_runtime_entrypoints_use_vite_port():
    playwright_config = (ROOT / "playwright.config.js").read_text(encoding="utf-8")
    vite_config = (ROOT / "vite.config.js").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    start_script = (ROOT / "start.bat").read_text(encoding="utf-8")
    tracked_runtime_docs = [playwright_config, vite_config, readme, claude, start_script]

    assert 'baseURL: "http://127.0.0.1:5173"' in playwright_config
    assert "npm run dev:frontend -- --host 127.0.0.1 --port 5173" in playwright_config
    assert 'url: "http://127.0.0.1:5173"' in playwright_config
    assert "port: 5173" in vite_config
    assert "http://127.0.0.1:5173" in readme
    assert "http://127.0.0.1:5173" in claude
    assert "npm run dev:frontend -- --host 127.0.0.1 --port 5173" in start_script
    assert "http://127.0.0.1:5173/?apiBase=http://127.0.0.1:8000" in start_script
    assert all("127.0.0.1:4173" not in content for content in tracked_runtime_docs)


def test_frontend_index_wires_css_js_and_app_shell():
    parser = parse_index()
    scripts = [attrs for tag, attrs in parser.elements if tag == "script"]
    ids = {attrs.get("id") for _, attrs in parser.elements if attrs.get("id")}

    assert any(script.get("src") == "/src/main.js" and script.get("type") == "module" for script in scripts)
    assert "app" in ids
    assert (FRONTEND_SRC / "App.vue").is_file()
    assert (FRONTEND_SRC / "main.js").is_file()
    assert (FRONTEND_SRC / "styles.css").is_file()
    assert THEME_CSS.is_file()
    assert GAME_STATE.is_file()
    assert APP_LAYOUT.is_file()
    assert BOARD_COMPONENT.is_file()
    assert STONE_COMPONENT.is_file()
    assert CONTROL_PANEL_COMPONENT.is_file()
    assert DIFFICULTY_SELECT_COMPONENT.is_file()
    assert THINKING_INDICATOR_COMPONENT.is_file()
    assert MOVE_HISTORY_COMPONENT.is_file()
    assert SEARCH_INFO_COMPONENT.is_file()
    assert ERROR_BANNER_COMPONENT.is_file()
    assert GAME_RESULT_COMPONENT.is_file()


def test_frontend_assets_define_board_and_api_placeholders():
    html = (FRONTEND / "index.html").read_text(encoding="utf-8")
    css = (FRONTEND_SRC / "styles.css").read_text(encoding="utf-8")
    theme = THEME_CSS.read_text(encoding="utf-8")
    app = (FRONTEND_SRC / "App.vue").read_text(encoding="utf-8")
    layout = APP_LAYOUT.read_text(encoding="utf-8")
    board_component = BOARD_COMPONENT.read_text(encoding="utf-8")
    stone_component = STONE_COMPONENT.read_text(encoding="utf-8")
    control_panel = CONTROL_PANEL_COMPONENT.read_text(encoding="utf-8")
    difficulty_select = DIFFICULTY_SELECT_COMPONENT.read_text(encoding="utf-8")
    thinking_indicator = THINKING_INDICATOR_COMPONENT.read_text(encoding="utf-8")
    move_history = MOVE_HISTORY_COMPONENT.read_text(encoding="utf-8")
    search_info = SEARCH_INFO_COMPONENT.read_text(encoding="utf-8")
    error_banner = ERROR_BANNER_COMPONENT.read_text(encoding="utf-8")
    game_result = GAME_RESULT_COMPONENT.read_text(encoding="utf-8")
    main = (FRONTEND_SRC / "main.js").read_text(encoding="utf-8")
    game_state = GAME_STATE.read_text(encoding="utf-8")

    assert 'data-api-base="http://127.0.0.1:8000"' in html
    assert "createApp(App" in main
    assert 'import "./theme.css";' in main
    assert 'from "./components/AppLayout.vue"' in app
    assert 'from "./components/Board.vue"' in app
    assert 'from "./components/ControlPanel.vue"' in app
    assert 'from "./components/DifficultySelect.vue"' in app
    assert 'from "./components/ErrorBanner.vue"' in app
    assert 'from "./components/GameResult.vue"' in app
    assert 'from "./components/MoveHistory.vue"' in app
    assert 'from "./components/SearchInfo.vue"' in app
    assert 'from "./components/ThinkingIndicator.vue"' in app
    assert 'from "./composables/useGameState"' in app
    assert "useGameState({" in app
    assert "<AppLayout>" in app
    assert "<Board" in app
    assert '<slot name="board"' in layout
    assert 'class="play-surface"' in layout
    assert 'class="side-panel"' in layout
    assert 'id="board"' in board_component
    assert 'class="cell"' in board_component
    assert 'from "./Stone.vue"' in board_component
    assert '<Stone v-if="role !== 0"' in board_component
    assert ':is-latest="isLatest(row, col)"' in board_component
    assert "@click=\"emit('play-move', row, col)\"" in board_component
    assert 'class="stone"' in stone_component
    assert "role === 1 ? 'black' : 'white'" in stone_component
    assert "'is-latest': isLatest" in stone_component
    assert "<ControlPanel" in app
    assert 'id="start-button"' in control_panel
    assert 'id="undo-button"' in control_panel
    assert 'id="end-button"' in control_panel
    assert 'id="restart-button"' in control_panel
    assert "emit('start-game')" in control_panel
    assert "emit('undo-move')" in control_panel
    assert "emit('end-game')" in control_panel
    assert "emit('restart-game')" in control_panel
    assert "<DifficultySelect" in app
    assert 'v-model:depth="state.settings.depth"' in app
    assert 'v-model:difficulty="state.settings.difficulty"' in app
    assert "DIFFICULTY_LEVELS" in difficulty_select
    assert ':id="`difficulty-${level.id}`"' in difficulty_select
    assert '{ id: "easy"' in difficulty_select
    assert '{ id: "normal"' in difficulty_select
    assert '{ id: "hard"' in difficulty_select
    assert '{ id: "custom"' in difficulty_select
    assert "depth: 2" in difficulty_select
    assert "depth: 4" in difficulty_select
    assert "depth: 6" in difficulty_select
    assert "<ThinkingIndicator" in app
    assert ':is-thinking="state.isBusy && state.status === \'AI 思考\'"' in app
    assert ':metrics="state.searchMetrics"' in app
    assert 'id="thinking-indicator"' in thinking_indicator
    assert 'id="thinking-state-value"' in thinking_indicator
    assert 'id="thinking-elapsed-value"' in thinking_indicator
    assert 'id="thinking-nodes-value"' in thinking_indicator
    assert 'id="thinking-prunes-value"' in thinking_indicator
    assert "elapsed_ms" in thinking_indicator
    assert '"nodes"' in thinking_indicator
    assert '"prunes"' in thinking_indicator
    assert "<MoveHistory" in app
    assert ':moves="state.history"' in app
    assert 'id="move-list"' in move_history
    assert 'id="move-empty"' in move_history
    assert "moves.length === 0" in move_history
    assert "roleName(move.role)" in move_history
    assert "move.i + 1" in move_history
    assert "move.j + 1" in move_history
    assert "<SearchInfo" in app
    assert ':best-path="state.bestPath"' in app
    assert ':current-depth="state.currentDepth"' in app
    assert ':metrics="state.searchMetrics"' in app
    assert ':score="state.score"' in app
    assert 'id="ai-score-value"' in search_info
    assert 'id="ai-depth-value"' in search_info
    assert 'id="best-path-value"' in search_info
    assert 'id="search-nodes-value"' in search_info
    assert 'id="search-prunes-value"' in search_info
    assert 'id="search-cache-hits-value"' in search_info
    assert '"cache_hits"' in search_info
    assert "function formatPath(path)" in search_info
    assert "<ErrorBanner" in app
    assert ':message="state.errorMessage"' in app
    assert '@dismiss="dismissError"' in app
    assert 'id="error-banner"' in error_banner
    assert 'id="error-message"' in error_banner
    assert 'id="error-dismiss-button"' in error_banner
    assert 'role="alert"' in error_banner
    assert "<GameResult" in app
    assert ':winner="state.winner"' in app
    assert ':is-game-over="state.isGameOver"' in app
    assert ':can-restart="canRestart"' in app
    assert '@restart-game="restartGame"' in app
    assert 'id="game-result"' in game_result
    assert 'id="game-result-value"' in game_result
    assert 'id="game-result-restart-button"' in game_result
    assert 'role="status"' in game_result
    assert 'resultLabel(winner)' in game_result
    assert 'id="board-size-input"' in app
    assert 'aria-describedby="board-size-hint"' in app
    assert "范围 5-25" in app
    assert 'id="search-depth-input"' in difficulty_select
    assert 'aria-describedby="search-depth-hint"' in difficulty_select
    assert "现有 depth 2/4/6" in difficulty_select
    assert 'id="api-base-input"' in app
    assert "?apiBase=" in app
    assert 'id="ai-first-input"' in app
    assert ".field-hint" in css
    assert "--space-md: 12px" in theme
    assert "--radius-sm: 4px" in theme
    assert "--shadow-panel:" in theme
    assert "--board-wood:" in theme
    assert "--focus-ring:" in theme
    assert "var(--radius-sm)" in css
    assert "var(--shadow-panel)" in css
    assert "var(--board-wood)" in css
    assert "button:focus-visible" in css
    assert ".app-shell" in css
    assert ".play-surface" in css
    assert ".side-panel" in css
    assert ".board-zone" in css
    assert "grid-template-columns: repeat(var(--board-size), 1fr)" in css
    assert ".cell:hover:not(:disabled)" in css
    assert ".cell.is-latest::after" in css
    assert "export const BOARD_SIZE = 15" in game_state
    assert 'export const DEFAULT_DIFFICULTY = "normal"' in game_state
    assert "reactive({" in game_state
    assert "difficulty: DEFAULT_DIFFICULTY" in game_state
    assert "state.board" in app


def test_frontend_calls_game_api_endpoints():
    app = (FRONTEND_SRC / "App.vue").read_text(encoding="utf-8")
    client = API_CLIENT.read_text(encoding="utf-8")
    game_state = GAME_STATE.read_text(encoding="utf-8")

    assert API_CLIENT.is_file()
    assert 'from "./composables/useGameState"' in app
    assert 'from "../api/client"' in game_state
    assert "createGameApi(readApiBase(defaultApiBase), defaultApiBase)" in game_state
    assert "fetch(" in client
    assert '"/api/health"' in client
    assert '"/api/games/start"' in client
    assert '`/api/games/${sessionId}/move`' in client
    assert '`/api/games/${sessionId}/undo`' in client
    assert '`/api/games/${sessionId}/end`' in client


def test_frontend_renders_api_snapshots():
    app = (FRONTEND_SRC / "App.vue").read_text(encoding="utf-8")
    board_component = BOARD_COMPONENT.read_text(encoding="utf-8")
    stone_component = STONE_COMPONENT.read_text(encoding="utf-8")
    move_history = MOVE_HISTORY_COMPONENT.read_text(encoding="utf-8")
    game_state = GAME_STATE.read_text(encoding="utf-8")

    assert "function applySnapshot(snapshot)" in game_state
    assert "snapshot.session_id" in game_state
    assert "snapshot.current_player" in game_state
    assert "snapshot.score" in game_state
    assert "snapshot.best_path" in game_state
    assert "snapshot.current_depth" in game_state
    assert "snapshot.search_metrics" in game_state
    assert "state.searchMetrics" in app
    assert "state.board[row]?.[col]" in game_state
    assert "latestMove" in game_state
    assert "'is-latest'" in board_component
    assert "stone-latest-dot" in stone_component
    assert "move.i + 1" in move_history
    assert "move.j + 1" in move_history
    search_info = SEARCH_INFO_COMPONENT.read_text(encoding="utf-8")
    assert "function formatPath(path)" in search_info
    assert "formatPath(bestPath)" in search_info


def test_frontend_handles_busy_state_and_non_json_errors():
    app = (FRONTEND_SRC / "App.vue").read_text(encoding="utf-8")
    client = API_CLIENT.read_text(encoding="utf-8")
    game_state = GAME_STATE.read_text(encoding="utf-8")

    assert "isBusy" in app
    assert "errorMessage" in game_state
    assert "function setError(message)" in game_state
    assert "function dismissError()" in game_state
    assert "setBusy(true)" in game_state
    assert "setBusy(false)" in game_state
    assert "response.text()" in client
    assert "JSON.parse" in client
    assert "throw new Error" in client
    assert "payload.detail" in client
    assert "catch (error)" in game_state
    assert "setError(error.message)" in game_state


def test_frontend_updates_controls_from_session_state():
    app = (FRONTEND_SRC / "App.vue").read_text(encoding="utf-8")
    control_panel = CONTROL_PANEL_COMPONENT.read_text(encoding="utf-8")
    game_state = GAME_STATE.read_text(encoding="utf-8")

    assert ':has-session="Boolean(state.sessionId)"' in app
    assert ':can-undo="state.history.length > 0"' in app
    assert "const canRestart = computed" in app
    assert "state.isGameOver" in app
    assert ':can-restart="canRestart"' in app
    assert ':disabled="isBusy || hasSession"' in control_panel
    assert ':disabled="isBusy || !hasSession || !canUndo"' in control_panel
    assert ':disabled="isBusy || !hasSession"' in control_panel
    assert ':disabled="isBusy || !canRestart"' in control_panel
    assert "async function restartGame()" in game_state
    assert "gameApi.endGame(state.sessionId)" in game_state
    assert "gameApi.startGame(state.settings)" in game_state
    assert "isGameOver: false" in game_state
    assert "function cellDisabled(row, col)" in game_state
    assert "state.isBusy || !state.sessionId || state.isGameOver" in game_state


def test_frontend_reads_start_settings_from_controls():
    app = (FRONTEND_SRC / "App.vue").read_text(encoding="utf-8")
    client = API_CLIENT.read_text(encoding="utf-8")
    game_state = GAME_STATE.read_text(encoding="utf-8")

    assert "function normalizeApiBase(candidate" in client
    assert "function readApiBase(" in game_state
    assert "new URLSearchParams(search)" in game_state
    assert 'params.get("apiBase")' in game_state
    assert 'url.protocol === "http:" || url.protocol === "https:"' in client
    assert "state.settings.apiBase = gameApi.setApiBase(state.settings.apiBase)" in game_state
    assert "fetch(`${base}${path}`" in client
    assert "size: Number(settings.size)" in client
    assert "depth: Number(settings.depth)" in client
    assert "ai_first: Boolean(settings.aiFirst)" in client
    assert "JSON.stringify({ position, depth })" in client


def test_frontend_tracks_status_in_state():
    game_state = GAME_STATE.read_text(encoding="utf-8")

    assert 'status: "待开始"' in game_state
    assert "state.status = text" in game_state
    assert 'setStatus(state.settings.aiFirst ? "AI 思考" : "连接中")' in game_state
    assert '"连接中"' in game_state
    assert 'setStatus("AI 思考")' in game_state
    assert 'setStatus("已结束")' in game_state
    assert "state.isGameOver = Boolean(state.winner)" in game_state
    assert "state.isGameOver = true" in game_state


def test_playwright_main_path_records_core_api_flow():
    spec = E2E_SPEC.read_text(encoding="utf-8")

    assert 'test("plays the main game path"' in spec
    assert "function apiCallSummary(request)" in spec
    assert 'request.method() === "OPTIONS"' in spec
    assert "const apiCalls = []" in spec
    assert 'expect(apiCalls[0]).toBe("POST /api/games/start")' in spec
    assert "/move" in spec
    assert "/undo" in spec
    assert "/end" in spec
    assert "expect(apiCalls).toHaveLength(4)" in spec
