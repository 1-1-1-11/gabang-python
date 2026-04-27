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
  const boardSizeInput = page.locator("#board-size-input");
  const searchDepthInput = page.locator("#search-depth-input");

  await expect(status).toHaveText("待开始");
  await expect(board.locator(".cell")).toHaveCount(225);
  await expect(startButton).toBeEnabled();
  await expect(undoButton).toBeDisabled();
  await expect(endButton).toBeDisabled();

  await boardSizeInput.fill("6");
  await searchDepthInput.fill("1");
  await startButton.click();

  await expect(status).toHaveText("进行中");
  await expect(page.locator("#size-value")).toHaveText("6 x 6");
  await expect(page.locator("#depth-value")).toHaveText("1");
  await expect(board.locator(".cell")).toHaveCount(36);
  await expect(startButton).toBeDisabled();
  await expect(undoButton).toBeDisabled();
  await expect(endButton).toBeEnabled();
  await expect(boardSizeInput).toBeDisabled();
  await expect(searchDepthInput).toBeDisabled();

  await board.locator('.cell[data-row="2"][data-col="2"]').click();

  await expect(status).toHaveText("进行中");
  await expect(board.locator(".stone")).toHaveCount(2);
  await expect(page.locator("#move-list li")).toHaveCount(2);
  await expect(page.locator("#move-list li").first()).toContainText("黑方 (3, 3)");
  await expect(page.locator("#move-list li").nth(1)).toContainText("白方");
  await expect(board.locator(".cell.is-latest")).toHaveCount(1);
  await expect(board.locator(".cell.is-latest .stone")).toHaveCount(1);
  await expect(board.locator('.cell[data-row="2"][data-col="2"]')).toBeDisabled();
  await board.locator('.cell[data-row="0"][data-col="0"]').hover();
  await expect(board.locator('.cell[data-row="0"][data-col="0"]')).toHaveCSS("cursor", "crosshair");
  await expect(board.locator('.cell[data-row="0"][data-col="0"]')).toHaveCSS("background-color", "rgba(255, 248, 234, 0.32)");
  await expect(undoButton).toBeEnabled();

  await undoButton.click();

  await expect(status).toHaveText("已悔棋");
  await expect(board.locator(".stone")).toHaveCount(0);
  await expect(board.locator(".cell.is-latest")).toHaveCount(0);
  await expect(page.locator("#move-list li")).toHaveCount(0);
  await expect(undoButton).toBeDisabled();

  await endButton.click();

  await expect(status).toHaveText("已结束");
  await expect(startButton).toBeEnabled();
  await expect(boardSizeInput).toBeEnabled();
  await expect(searchDepthInput).toBeEnabled();
  await expect(undoButton).toBeDisabled();
  await expect(endButton).toBeDisabled();
  await expect(board.locator(".cell").first()).toBeDisabled();
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
  const boardSizeInput = page.locator("#board-size-input");
  const searchDepthInput = page.locator("#search-depth-input");
  const aiFirstInput = page.locator("#ai-first-input");

  await boardSizeInput.fill("7");
  await searchDepthInput.fill("2");
  await aiFirstInput.check();
  await startButton.click();

  await expect(page.locator("#status")).toHaveText("连接中");
  await expect(startButton).toBeDisabled();
  await expect(undoButton).toBeDisabled();
  await expect(endButton).toBeDisabled();
  await expect(boardSizeInput).toBeDisabled();
  await expect(searchDepthInput).toBeDisabled();
  await expect(aiFirstInput).toBeDisabled();
  await expect(boardElement.locator(".cell").first()).toBeDisabled();

  await page.evaluate(() => document.querySelector("#start-button").click());
  expect(requestCount).toBe(1);

  releaseStart();

  await expect(page.locator("#status")).toHaveText("进行中");
  await expect(page.locator("#size-value")).toHaveText("7 x 7");
  await expect(page.locator("#depth-value")).toHaveText("2");
  await expect(boardElement.locator(".cell")).toHaveCount(49);
  await expect(endButton).toBeEnabled();
  expect(requestBody).toEqual({ size: 7, ai_first: true, depth: 2 });
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
  await page.locator("#search-depth-input").fill("1");
  await page.locator("#start-button").click();

  await expect(page.locator("#status")).toHaveText("服务暂不可用");
  await expect(page.locator("#start-button")).toBeEnabled();
  await expect(page.locator("#board-size-input")).toBeEnabled();
  await expect(page.locator("#search-depth-input")).toBeEnabled();
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
  await page.locator("#search-depth-input").fill("1");
  await page.locator("#start-button").click();

  await expect(page.locator("#status")).toHaveText("响应格式错误");
  await expect(page.locator("#start-button")).toBeEnabled();
  await expect(page.locator("#board-size-input")).toBeEnabled();
  await expect(page.locator("#search-depth-input")).toBeEnabled();
  await expect(page.locator("#undo-button")).toBeDisabled();
  await expect(page.locator("#end-button")).toBeDisabled();
});
