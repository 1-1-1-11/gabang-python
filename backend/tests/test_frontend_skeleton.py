from html.parser import HTMLParser
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"


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


def test_node_tooling_is_limited_to_e2e():
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    scripts = package.get("scripts", {})
    dependencies = package.get("dependencies", {})
    dev_dependencies = package.get("devDependencies", {})
    lockfile = (ROOT / "package-lock.json").read_text(encoding="utf-8")

    assert scripts == {
        "test:e2e": "playwright test",
        "test:e2e:headed": "playwright test --headed",
    }
    assert dependencies == {}
    assert set(dev_dependencies) == {"@playwright/test"}
    for forbidden in ("react", "react-dom", "vue", "vite", "webpack", "config-overrides"):
        assert forbidden not in dependencies
        assert forbidden not in dev_dependencies
        assert f'node_modules/{forbidden}' not in lockfile


def test_frontend_index_wires_css_js_and_app_shell():
    parser = parse_index()
    links = [attrs for tag, attrs in parser.elements if tag == "link"]
    scripts = [attrs for tag, attrs in parser.elements if tag == "script"]
    ids = {attrs.get("id") for _, attrs in parser.elements if attrs.get("id")}

    assert any(link.get("href") == "styles.css" for link in links)
    assert any(script.get("src") == "app.js" and script.get("type") == "module" for script in scripts)
    assert {
        "app",
        "board",
        "status",
        "move-list",
        "start-button",
        "undo-button",
        "end-button",
        "board-size-input",
        "search-depth-input",
        "ai-first-input",
        "api-base-input",
        "board-size-hint",
        "search-depth-hint",
        "api-base-hint",
        "size-value",
        "current-player-value",
        "winner-value",
        "ai-score-value",
        "ai-depth-value",
        "best-path-value",
    }.issubset(ids)


def test_frontend_assets_define_board_and_api_placeholders():
    html = (FRONTEND / "index.html").read_text(encoding="utf-8")
    css = (FRONTEND / "styles.css").read_text(encoding="utf-8")
    js = (FRONTEND / "app.js").read_text(encoding="utf-8")

    assert 'data-api-base="http://127.0.0.1:8000"' in html
    assert 'id="board-size-input"' in html
    assert 'aria-describedby="board-size-hint"' in html
    assert "范围 5-25" in html
    assert 'id="search-depth-input"' in html
    assert 'aria-describedby="search-depth-hint"' in html
    assert "深度越高 AI 思考越慢" in html
    assert 'id="api-base-input"' in html
    assert "?apiBase=" in html
    assert 'id="ai-first-input"' in html
    assert ".field-hint" in css
    assert "grid-template-columns: repeat(var(--board-size), 1fr)" in css
    assert ".cell:hover:not(:disabled)" in css
    assert ".cell.is-latest::after" in css
    assert "const BOARD_SIZE = 15" in js
    assert "renderBoard" in js


def test_frontend_calls_game_api_endpoints():
    js = (FRONTEND / "app.js").read_text(encoding="utf-8")

    assert "fetch(" in js
    assert '"/api/games/start"' in js
    assert '`/api/games/${state.sessionId}/move`' in js
    assert '`/api/games/${state.sessionId}/undo`' in js
    assert '`/api/games/${state.sessionId}/end`' in js


def test_frontend_renders_api_snapshots():
    js = (FRONTEND / "app.js").read_text(encoding="utf-8")

    assert "function applySnapshot(snapshot)" in js
    assert "snapshot.session_id" in js
    assert "snapshot.current_player" in js
    assert "snapshot.score" in js
    assert "snapshot.best_path" in js
    assert "snapshot.current_depth" in js
    assert "state.board[row][col]" in js
    assert "latestMove()" in js
    assert "cell.classList.add(\"is-latest\")" in js
    assert "move.i + 1" in js
    assert "move.j + 1" in js
    assert "function formatPath(path)" in js
    assert "bestPathValue.textContent = formatPath(state.bestPath)" in js


def test_frontend_handles_busy_state_and_non_json_errors():
    js = (FRONTEND / "app.js").read_text(encoding="utf-8")

    assert "isBusy" in js
    assert "setBusy(true)" in js
    assert "setBusy(false)" in js
    assert "response.text()" in js
    assert "JSON.parse" in js
    assert "响应格式错误" in js
    assert "catch (error)" in js
    assert "setStatus(error.message)" in js


def test_frontend_updates_controls_from_session_state():
    js = (FRONTEND / "app.js").read_text(encoding="utf-8")

    assert "function updateControls()" in js
    assert "startButton.disabled = state.isBusy || Boolean(state.sessionId)" in js
    assert "undoButton.disabled = state.isBusy || !state.sessionId || state.history.length === 0" in js
    assert "endButton.disabled = state.isBusy || !state.sessionId" in js
    assert "boardSizeInput.disabled = state.isBusy || Boolean(state.sessionId)" in js
    assert "searchDepthInput.disabled = state.isBusy || Boolean(state.sessionId)" in js
    assert "apiBaseInput.disabled = state.isBusy || Boolean(state.sessionId)" in js
    assert "aiFirstInput.disabled = state.isBusy || Boolean(state.sessionId)" in js
    assert "for (const cell of boardElement.querySelectorAll" in js
    assert "cell.disabled = state.isBusy || !state.sessionId || Boolean(state.winner)" in js
    assert "updateControls();" in js


def test_frontend_reads_start_settings_from_controls():
    js = (FRONTEND / "app.js").read_text(encoding="utf-8")

    assert "function normalizeApiBase(candidate)" in js
    assert "function readApiBase()" in js
    assert "new URLSearchParams(window.location.search)" in js
    assert 'params.get("apiBase")' in js
    assert 'url.protocol === "http:" || url.protocol === "https:"' in js
    assert "apiBaseInput.value = readApiBase()" in js
    assert "apiBaseInput.disabled = state.isBusy || Boolean(state.sessionId)" in js
    assert "apiBaseInput.value = normalizeApiBase(apiBaseInput.value)" in js
    assert "fetch(`${apiBaseInput.value}${path}`" in js
    assert "function readGameSettings()" in js
    assert "size: Number(boardSizeInput.value)" in js
    assert "depth: Number(searchDepthInput.value)" in js
    assert "aiFirst: aiFirstInput.checked" in js
    assert "JSON.stringify({ size: settings.size, ai_first: settings.aiFirst, depth: settings.depth })" in js
    assert "JSON.stringify({ position: [row, col], depth: state.depth })" in js


def test_frontend_tracks_status_in_state():
    js = (FRONTEND / "app.js").read_text(encoding="utf-8")

    assert 'status: "待开始"' in js
    assert "state.status = text" in js
    assert 'setStatus("连接中")' in js
    assert 'setStatus("AI 思考")' in js
    assert 'setStatus("已结束")' in js