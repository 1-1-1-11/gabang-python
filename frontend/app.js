const BOARD_SIZE = 15;

const boardElement = document.querySelector("#board");
const statusElement = document.querySelector("#status");
const moveListElement = document.querySelector("#move-list");

const previewMoves = [
  { row: 7, col: 7, role: "black" },
  { row: 7, col: 8, role: "white" },
  { row: 8, col: 7, role: "black" },
];

function createCell(row, col) {
  const cell = document.createElement("button");
  cell.className = "cell";
  cell.type = "button";
  cell.setAttribute("role", "gridcell");
  cell.setAttribute("aria-label", `row ${row + 1}, column ${col + 1}`);
  cell.dataset.row = String(row);
  cell.dataset.col = String(col);
  return cell;
}

function placePreviewStone(cell, role) {
  const stone = document.createElement("span");
  stone.className = `stone ${role}`;
  stone.setAttribute("aria-hidden", "true");
  cell.append(stone);
}

function renderMoveList() {
  moveListElement.replaceChildren(
    ...previewMoves.map((move, index) => {
      const item = document.createElement("li");
      item.textContent = `${index + 1}. ${move.role} (${move.row}, ${move.col})`;
      return item;
    }),
  );
}

function renderBoard() {
  const movesByCoordinate = new Map(previewMoves.map((move) => [`${move.row}:${move.col}`, move.role]));
  const cells = [];

  for (let row = 0; row < BOARD_SIZE; row += 1) {
    for (let col = 0; col < BOARD_SIZE; col += 1) {
      const cell = createCell(row, col);
      const previewRole = movesByCoordinate.get(`${row}:${col}`);
      if (previewRole) {
        placePreviewStone(cell, previewRole);
      }
      cells.push(cell);
    }
  }

  boardElement.replaceChildren(...cells);
  statusElement.textContent = "骨架就绪";
  renderMoveList();
}

renderBoard();
