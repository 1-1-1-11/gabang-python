const { expect, test } = require("@playwright/test");

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
  await expect(page.locator("#move-list li").first()).toContainText("黑方 (2, 2)");
  await expect(page.locator("#move-list li").nth(1)).toContainText("白方");
  await expect(undoButton).toBeEnabled();

  await undoButton.click();

  await expect(status).toHaveText("已悔棋");
  await expect(board.locator(".stone")).toHaveCount(0);
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
