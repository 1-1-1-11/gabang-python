from html.parser import HTMLParser
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"
FRONTEND_SRC = FRONTEND / "src"


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
    scripts = package.get("scripts", {})
    dependencies = package.get("dependencies", {})
    dev_dependencies = package.get("devDependencies", {})
    lockfile = (ROOT / "package-lock.json").read_text(encoding="utf-8")

    assert scripts["dev:frontend"] == "vite"
    assert scripts["build"] == "vite build"
    assert scripts["preview:frontend"] == "vite preview"
    assert scripts["test:e2e"] == "playwright test"
    assert scripts["test:e2e:headed"] == "playwright test --headed"
    assert set(dependencies) == {"vue"}
    assert {"@playwright/test", "@vitejs/plugin-vue", "vite"}.issubset(dev_dependencies)
    for forbidden in ("react", "react-dom", "webpack", "config-overrides"):
        assert forbidden not in dependencies
        assert forbidden not in dev_dependencies
        assert f'node_modules/{forbidden}' not in lockfile


def test_frontend_index_wires_css_js_and_app_shell():
    parser = parse_index()
    scripts = [attrs for tag, attrs in parser.elements if tag == "script"]
    ids = {attrs.get("id") for _, attrs in parser.elements if attrs.get("id")}

    assert any(script.get("src") == "/src/main.js" and script.get("type") == "module" for script in scripts)
    assert "app" in ids
    assert (FRONTEND_SRC / "App.vue").is_file()
    assert (FRONTEND_SRC / "main.js").is_file()
    assert (FRONTEND_SRC / "styles.css").is_file()


def test_frontend_assets_define_board_and_api_placeholders():
    html = (FRONTEND / "index.html").read_text(encoding="utf-8")
    css = (FRONTEND_SRC / "styles.css").read_text(encoding="utf-8")
    app = (FRONTEND_SRC / "App.vue").read_text(encoding="utf-8")
    main = (FRONTEND_SRC / "main.js").read_text(encoding="utf-8")

    assert 'data-api-base="http://127.0.0.1:8000"' in html
    assert "createApp(App" in main
    assert 'id="board-size-input"' in app
    assert 'aria-describedby="board-size-hint"' in app
    assert "范围 5-25" in app
    assert 'id="search-depth-input"' in app
    assert 'aria-describedby="search-depth-hint"' in app
    assert "深度越高 AI 思考越慢" in app
    assert 'id="api-base-input"' in app
    assert "?apiBase=" in app
    assert 'id="ai-first-input"' in app
    assert ".field-hint" in css
    assert "grid-template-columns: repeat(var(--board-size), 1fr)" in css
    assert ".cell:hover:not(:disabled)" in css
    assert ".cell.is-latest::after" in css
    assert "const BOARD_SIZE = 15" in app
    assert "state.board" in app


def test_frontend_calls_game_api_endpoints():
    app = (FRONTEND_SRC / "App.vue").read_text(encoding="utf-8")

    assert "fetch(" in app
    assert '"/api/games/start"' in app
    assert '`/api/games/${state.sessionId}/move`' in app
    assert '`/api/games/${state.sessionId}/undo`' in app
    assert '`/api/games/${state.sessionId}/end`' in app


def test_frontend_renders_api_snapshots():
    app = (FRONTEND_SRC / "App.vue").read_text(encoding="utf-8")

    assert "function applySnapshot(snapshot)" in app
    assert "snapshot.session_id" in app
    assert "snapshot.current_player" in app
    assert "snapshot.score" in app
    assert "snapshot.best_path" in app
    assert "snapshot.current_depth" in app
    assert "state.board[row]?.[col]" in app
    assert "latestMove" in app
    assert "'is-latest'" in app
    assert "move.i + 1" in app
    assert "move.j + 1" in app
    assert "function formatPath(path)" in app
    assert "formatPath(state.bestPath)" in app


def test_frontend_handles_busy_state_and_non_json_errors():
    app = (FRONTEND_SRC / "App.vue").read_text(encoding="utf-8")

    assert "isBusy" in app
    assert "setBusy(true)" in app
    assert "setBusy(false)" in app
    assert "response.text()" in app
    assert "JSON.parse" in app
    assert "响应格式错误" in app
    assert "catch (error)" in app
    assert "setStatus(error.message)" in app


def test_frontend_updates_controls_from_session_state():
    app = (FRONTEND_SRC / "App.vue").read_text(encoding="utf-8")

    assert ':disabled="state.isBusy || Boolean(state.sessionId)"' in app
    assert ':disabled="state.isBusy || !state.sessionId || state.history.length === 0"' in app
    assert ':disabled="state.isBusy || !state.sessionId"' in app
    assert "function cellDisabled(row, col)" in app
    assert "state.isBusy || !state.sessionId || Boolean(state.winner)" in app


def test_frontend_reads_start_settings_from_controls():
    app = (FRONTEND_SRC / "App.vue").read_text(encoding="utf-8")

    assert "function normalizeApiBase(candidate)" in app
    assert "function readApiBase()" in app
    assert "new URLSearchParams(window.location.search)" in app
    assert 'params.get("apiBase")' in app
    assert 'url.protocol === "http:" || url.protocol === "https:"' in app
    assert "state.settings.apiBase = normalizeApiBase(state.settings.apiBase)" in app
    assert "fetch(`${state.settings.apiBase}${path}`" in app
    assert "size: Number(state.settings.size)" in app
    assert "depth: Number(state.settings.depth)" in app
    assert "ai_first: state.settings.aiFirst" in app
    assert "JSON.stringify({ position: [row, col], depth: state.depth })" in app


def test_frontend_tracks_status_in_state():
    app = (FRONTEND_SRC / "App.vue").read_text(encoding="utf-8")

    assert 'status: "待开始"' in app
    assert "state.status = text" in app
    assert 'setStatus("连接中")' in app
    assert 'setStatus("AI 思考")' in app
    assert 'setStatus("已结束")' in app
