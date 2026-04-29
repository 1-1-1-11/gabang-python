const { expect, test } = require("@playwright/test");

function board(size) {
  return Array.from({ length: size }, () => Array(size).fill(0));
}

function snapshot(overrides = {}) {
  const size = overrides.size ?? 6;
  return {
    session_id: "e2e-session",
    board: board(size),
    history: [],
    current_player: 1,
    winner: null,
    size,
    score: null,
    best_path: [],
    current_depth: overrides.current_depth ?? 1,
    search_metrics: overrides.search_metrics ?? null,
    ...overrides,
  };
}

test("plays the main game path", async ({ page }) => {
  await page.goto("/");

  const board = page.locator("#board");
  const status = page.locator("#status");
  const startButton = page.locator("#start-button");
  const undoButton = page.locator("#undo-button");
  const endButton = page.locator("#end-button");
  const restartButton = page.locator("#restart-button");
  const boardSizeInput = page.locator("#board-size-input");
  const searchDepthInput = page.locator("#search-depth-input");
  const apiBaseInput = page.locator("#api-base-input");

  await expect(page.locator("#board-size-hint")).toContainText("范围 5-25");
  await expect(page.locator("#search-depth-hint")).toContainText("现有 depth 2/4/6");
  await expect(page.locator("#api-base-hint")).toContainText("?apiBase=");
  await expect(apiBaseInput).toHaveValue("http://127.0.0.1:8000");
  await expect(page.locator("#difficulty-normal")).toHaveAttribute("aria-pressed", "true");
  await expect(searchDepthInput).toHaveCount(0);

  await expect(status).toHaveText("待开始");
  await expect(board.locator(".cell")).toHaveCount(225);
  await expect(page.locator("#ai-score-value")).toHaveText("-");
  await expect(page.locator("#ai-depth-value")).toHaveText("-");
  await expect(page.locator("#best-path-value")).toHaveText("-");
  await expect(page.locator("#thinking-state-value")).toHaveText("AI 待命");
  await expect(page.locator("#thinking-elapsed-value")).toHaveText("-");
  await expect(page.locator("#thinking-nodes-value")).toHaveText("-");
  await expect(page.locator("#thinking-prunes-value")).toHaveText("-");
  await expect(page.locator("#move-empty")).toHaveText("暂无落子");
  await expect(startButton).toBeEnabled();
  await expect(undoButton).toBeDisabled();
  await expect(endButton).toBeDisabled();
  await expect(restartButton).toBeDisabled();

  await boardSizeInput.fill("6");
  await page.locator("#difficulty-easy").click();
  await expect(page.locator("#difficulty-easy")).toHaveAttribute("aria-pressed", "true");
  await startButton.click();

  await expect(status).toHaveText("进行中");
  await expect(page.locator("#size-value")).toHaveText("6 x 6");
  await expect(page.locator("#depth-value")).toHaveText("2");
  await expect(board.locator(".cell")).toHaveCount(36);
  await expect(startButton).toBeDisabled();
  await expect(undoButton).toBeDisabled();
  await expect(endButton).toBeEnabled();
  await expect(restartButton).toBeEnabled();
  await expect(boardSizeInput).toBeDisabled();
  await expect(page.locator("#difficulty-easy")).toBeDisabled();
  await expect(apiBaseInput).toBeDisabled();

  await board.locator('.cell[data-row="2"][data-col="2"]').click();

  await expect(status).toHaveText("进行中");
  await expect(page.locator("#ai-score-value")).not.toHaveText("-");
  await expect(page.locator("#ai-depth-value")).toHaveText("2");
  await expect(page.locator("#best-path-value")).toHaveText(/^(?:\([1-9]\d*, [1-9]\d*\))(?: → \([1-9]\d*, [1-9]\d*\))*$/);
  await expect(page.locator("#thinking-state-value")).toHaveText("AI 待命");
  await expect(page.locator("#thinking-nodes-value")).not.toHaveText("-");
  await expect(board.locator(".stone")).toHaveCount(2);
  await expect(board.locator(".stone.black")).toHaveCount(1);
  await expect(board.locator(".stone.white")).toHaveCount(1);
  await expect(board.locator(".stone.is-latest")).toHaveCount(1);
  await expect(board.locator(".cell.is-latest .stone-latest-dot")).toHaveCount(1);
  await expect(page.locator("#move-list li")).toHaveCount(2);
  await expect(page.locator("#move-empty")).toHaveCount(0);
  await expect(page.locator("#move-list li").first()).toContainText("黑方 (3, 3)");
  await expect(page.locator("#move-list li").nth(1)).toContainText("白方");
  await expect(board.locator(".cell.is-latest")).toHaveCount(1);
  await expect(board.locator(".cell.is-latest .stone")).toHaveCount(1);
  await expect(board.locator('.cell[data-row="2"][data-col="2"]')).toBeDisabled();
  await board.locator('.cell[data-row="0"][data-col="0"]').hover();
  await expect(board.locator('.cell[data-row="0"][data-col="0"]')).toHaveCSS("cursor", "crosshair");
  await expect(board.locator('.cell[data-row="0"][data-col="0"]')).toHaveCSS("background-color", "rgba(255, 248, 234, 0.32)");
  await expect(undoButton).toBeEnabled();
  await expect(restartButton).toBeEnabled();

  await undoButton.click();

  await expect(status).toHaveText("已悔棋");
  await expect(board.locator(".stone")).toHaveCount(0);
  await expect(board.locator(".cell.is-latest")).toHaveCount(0);
  await expect(page.locator("#move-list li")).toHaveCount(0);
  await expect(page.locator("#move-empty")).toHaveText("暂无落子");
  await expect(undoButton).toBeDisabled();
  await expect(restartButton).toBeEnabled();

  await endButton.click();

  await expect(status).toHaveText("已结束");
  await expect(startButton).toBeEnabled();
  await expect(boardSizeInput).toBeEnabled();
  await expect(page.locator("#difficulty-easy")).toBeEnabled();
  await expect(apiBaseInput).toBeEnabled();
  await expect(undoButton).toBeDisabled();
  await expect(endButton).toBeDisabled();
  await expect(restartButton).toBeDisabled();
  await expect(board.locator(".cell").first()).toBeDisabled();
});

test("restarts the active game from the control panel", async ({ page }) => {
  let startCount = 0;
  let endCount = 0;
  const requestOrder = [];

  await page.route("**/api/games/start", async (route) => {
    startCount += 1;
    requestOrder.push("start");
    const requestBody = route.request().postDataJSON();
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(snapshot({ size: requestBody.size, current_depth: requestBody.depth })),
    });
  });

  await page.route("**/api/games/e2e-session/end", async (route) => {
    endCount += 1;
    requestOrder.push("end");
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(snapshot({ winner: 0 })),
    });
  });

  await page.goto("/");
  await page.locator("#board-size-input").fill("6");
  await page.locator("#difficulty-easy").click();
  await page.locator("#start-button").click();

  await expect(page.locator("#status")).toHaveText("进行中");
  await expect(page.locator("#restart-button")).toBeEnabled();

  await page.locator("#restart-button").click();

  await expect(page.locator("#status")).toHaveText("进行中");
  await expect(page.locator("#board .cell")).toHaveCount(36);
  await expect(page.locator("#restart-button")).toBeEnabled();
  expect(startCount).toBe(2);
  expect(endCount).toBe(1);
  expect(requestOrder).toEqual(["start", "end", "start"]);
});

test("keeps the page layout stable across desktop and narrow viewports", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto("/");

  const desktopPlaySurface = await page.locator(".play-surface").boundingBox();
  const desktopSidePanel = await page.locator(".side-panel").boundingBox();
  expect(desktopPlaySurface).not.toBeNull();
  expect(desktopSidePanel).not.toBeNull();
  expect(desktopSidePanel.x).toBeGreaterThan(desktopPlaySurface.x + desktopPlaySurface.width - 1);

  await page.setViewportSize({ width: 390, height: 844 });

  const mobilePlaySurface = await page.locator(".play-surface").boundingBox();
  const mobileSidePanel = await page.locator(".side-panel").boundingBox();
  const mobileBoard = await page.locator("#board").boundingBox();
  expect(mobilePlaySurface).not.toBeNull();
  expect(mobileSidePanel).not.toBeNull();
  expect(mobileBoard).not.toBeNull();
  expect(mobileSidePanel.y).toBeGreaterThan(mobilePlaySurface.y + mobilePlaySurface.height - 1);
  expect(mobileBoard.width).toBeLessThanOrEqual(390);

  const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
  expect(scrollWidth).toBeLessThanOrEqual(390);
});

test("sends settings and disables controls while starting", async ({ page }) => {
  let requestCount = 0;
  let requestBody;
  let releaseStart;
  const startCanFinish = new Promise((resolve) => {
    releaseStart = resolve;
  });

  await page.route("**/api/games/start", async (route) => {
    requestCount += 1;
    requestBody = route.request().postDataJSON();
    await startCanFinish;
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(snapshot({ size: requestBody.size, current_depth: requestBody.depth })),
    });
  });

  await page.goto("/");

  const boardElement = page.locator("#board");
  const startButton = page.locator("#start-button");
  const undoButton = page.locator("#undo-button");
  const endButton = page.locator("#end-button");
  const restartButton = page.locator("#restart-button");
  const boardSizeInput = page.locator("#board-size-input");
  const apiBaseInput = page.locator("#api-base-input");
  const aiFirstInput = page.locator("#ai-first-input");

  await boardSizeInput.fill("7");
  await page.locator("#difficulty-hard").click();
  await aiFirstInput.check();
  await startButton.click();

  await expect(page.locator("#status")).toHaveText("AI 思考");
  await expect(page.locator("#thinking-state-value")).toHaveText("AI 思考中");
  await expect(startButton).toBeDisabled();
  await expect(undoButton).toBeDisabled();
  await expect(endButton).toBeDisabled();
  await expect(restartButton).toBeDisabled();
  await expect(boardSizeInput).toBeDisabled();
  await expect(page.locator("#difficulty-hard")).toBeDisabled();
  await expect(apiBaseInput).toBeDisabled();
  await expect(aiFirstInput).toBeDisabled();
  await expect(boardElement.locator(".cell").first()).toBeDisabled();

  await page.evaluate(() => document.querySelector("#start-button").click());
  expect(requestCount).toBe(1);

  releaseStart();

  await expect(page.locator("#status")).toHaveText("进行中");
  await expect(page.locator("#size-value")).toHaveText("7 x 7");
  await expect(page.locator("#depth-value")).toHaveText("6");
  await expect(boardElement.locator(".cell")).toHaveCount(49);
  await expect(endButton).toBeEnabled();
  await expect(restartButton).toBeEnabled();
  expect(requestBody).toEqual({ size: 7, ai_first: true, depth: 6 });
});

test("shows thinking state while AI move is pending and then renders search metrics", async ({ page }) => {
  let releaseMove;
  const moveCanFinish = new Promise((resolve) => {
    releaseMove = resolve;
  });

  await page.route("**/api/games/start", async (route) => {
    const requestBody = route.request().postDataJSON();
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(snapshot({ size: requestBody.size, current_depth: requestBody.depth })),
    });
  });

  await page.route("**/api/games/e2e-session/move", async (route) => {
    await moveCanFinish;
    const movedBoard = board(6);
    movedBoard[2][2] = 1;
    movedBoard[2][3] = -1;
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(snapshot({
        board: movedBoard,
        history: [
          { i: 2, j: 2, role: 1 },
          { i: 2, j: 3, role: -1 },
        ],
        score: 16,
        best_path: [[2, 3]],
        current_depth: 2,
        search_metrics: {
          nodes: 42,
          prunes: 5,
          cache_hits: 3,
          cache_stores: 7,
          candidate_moves: 12,
          leaf_nodes: 18,
          max_depth: 2,
          elapsed_ms: 12.34,
        },
      })),
    });
  });

  await page.goto("/");
  await page.locator("#board-size-input").fill("6");
  await page.locator("#difficulty-easy").click();
  await page.locator("#start-button").click();
  await page.locator('#board .cell[data-row="2"][data-col="2"]').click();

  await expect(page.locator("#status")).toHaveText("AI 思考");
  await expect(page.locator("#thinking-state-value")).toHaveText("AI 思考中");
  await expect(page.locator("#thinking-indicator")).toHaveClass(/is-thinking/);

  releaseMove();

  await expect(page.locator("#status")).toHaveText("进行中");
  await expect(page.locator("#thinking-state-value")).toHaveText("AI 待命");
  await expect(page.locator("#thinking-elapsed-value")).toHaveText(/\d+\.\d ms/);
  await expect(page.locator("#thinking-elapsed-value")).not.toHaveText("-");
  await expect(page.locator("#thinking-nodes-value")).toHaveText("42");
  await expect(page.locator("#thinking-prunes-value")).toHaveText("5");
});

test("maps difficulty presets and custom depth to existing depth setting", async ({ page }) => {
  let requestBody;

  await page.route("**/api/games/start", async (route) => {
    requestBody = route.request().postDataJSON();
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(snapshot({ size: requestBody.size, current_depth: requestBody.depth })),
    });
  });

  await page.goto("/");

  await expect(page.locator("#search-depth-input")).toHaveCount(0);
  await page.locator("#difficulty-easy").click();
  await expect(page.locator("#difficulty-easy")).toHaveAttribute("aria-pressed", "true");
  await page.locator("#difficulty-hard").click();
  await expect(page.locator("#difficulty-hard")).toHaveAttribute("aria-pressed", "true");
  await page.locator("#difficulty-custom").click();
  await expect(page.locator("#search-depth-input")).toBeVisible();
  await page.locator("#search-depth-input").fill("3");
  await page.locator("#board-size-input").fill("6");
  await page.locator("#start-button").click();

  await expect(page.locator("#status")).toHaveText("进行中");
  await expect(page.locator("#depth-value")).toHaveText("3");
  expect(requestBody).toEqual({ size: 6, ai_first: false, depth: 3 });
});

test("uses api base from query string", async ({ page }) => {
  let requestedUrl;

  await page.route("http://127.0.0.1:8000/api/games/start", async (route) => {
    requestedUrl = route.request().url();
    const requestBody = route.request().postDataJSON();
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(snapshot({ size: requestBody.size, current_depth: requestBody.depth })),
    });
  });

  await page.goto("/?apiBase=http://127.0.0.1:8000/api/ignored");

  await expect(page.locator("#api-base-input")).toHaveValue("http://127.0.0.1:8000");
  await page.locator("#board-size-input").fill("6");
  await page.locator("#difficulty-easy").click();
  await page.locator("#start-button").click();

  await expect(page.locator("#status")).toHaveText("进行中");
  expect(requestedUrl).toBe("http://127.0.0.1:8000/api/games/start");
});
test("recovers controls after json error responses", async ({ page }) => {
  await page.route("**/api/games/start", async (route) => {
    await route.fulfill({
      status: 500,
      contentType: "application/json",
      body: JSON.stringify({ detail: "服务暂不可用" }),
    });
  });

  await page.goto("/");
  await page.locator("#board-size-input").fill("6");
  await page.locator("#difficulty-easy").click();
  await page.locator("#start-button").click();

  await expect(page.locator("#status")).toHaveText("服务暂不可用");
  await expect(page.locator("#start-button")).toBeEnabled();
  await expect(page.locator("#board-size-input")).toBeEnabled();
  await expect(page.locator("#difficulty-easy")).toBeEnabled();
  await expect(page.locator("#api-base-input")).toBeEnabled();
  await expect(page.locator("#undo-button")).toBeDisabled();
  await expect(page.locator("#end-button")).toBeDisabled();
});

test("recovers controls after non-json responses", async ({ page }) => {
  await page.route("**/api/games/start", async (route) => {
    await route.fulfill({
      status: 502,
      contentType: "text/plain",
      body: "bad gateway",
    });
  });

  await page.goto("/");
  await page.locator("#board-size-input").fill("6");
  await page.locator("#difficulty-easy").click();
  await page.locator("#start-button").click();

  await expect(page.locator("#status")).toHaveText("响应格式错误");
  await expect(page.locator("#start-button")).toBeEnabled();
  await expect(page.locator("#board-size-input")).toBeEnabled();
  await expect(page.locator("#difficulty-easy")).toBeEnabled();
  await expect(page.locator("#api-base-input")).toBeEnabled();
  await expect(page.locator("#undo-button")).toBeDisabled();
  await expect(page.locator("#end-button")).toBeDisabled();
});
