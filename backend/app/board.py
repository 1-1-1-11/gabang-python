from collections.abc import Sequence

from backend.app.evaluation import FIVE, Evaluate
from backend.app.zobrist import Zobrist


class Board:
    def __init__(self, size: int = 15, first_role: int = 1):
        if size <= 0:
            raise ValueError("Board size must be positive.")
        if first_role not in (1, -1):
            raise ValueError("first_role must be 1 or -1.")

        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.first_role = first_role
        self.current_player = first_role
        self.history: list[dict[str, int]] = []
        self._winner = 0
        self._winner_history: list[int] = []
        self.zobrist = Zobrist(size)
        self.evaluator = Evaluate(size)

    def put(self, i: int, j: int, role: int | None = None) -> bool:
        if role is None:
            role = self.current_player
        if role not in (1, -1):
            return False
        if not self._is_inside(i, j):
            return False
        if self.board[i][j] != 0:
            return False

        self.board[i][j] = role
        self.history.append({"i": i, "j": j, "role": role})
        self._winner_history.append(self._winner)
        self.zobrist.toggle_piece(i, j, role)
        self.evaluator.move(i, j, role)
        if self._winner == 0 and self._is_winning_move(i, j, role):
            self._winner = role
        self.current_player = -role
        return True

    def undo(self) -> bool:
        if not self.history:
            return False

        move = self.history.pop()
        self.board[move["i"]][move["j"]] = 0
        self.zobrist.toggle_piece(move["i"], move["j"], move["role"])
        self.evaluator.undo(move["i"], move["j"])
        self._winner = self._winner_history.pop()
        # Restore the player who made the undone move.
        self.current_player = move["role"]
        return True

    def get_valid_moves(self) -> list[list[int]]:
        return [
            [i, j]
            for i in range(self.size)
            for j in range(self.size)
            if self.board[i][j] == 0
        ]

    def is_game_over(self) -> bool:
        if self.get_winner() != 0:
            return True
        return not any(cell == 0 for row in self.board for cell in row)

    def get_winner(self) -> int:
        return self._winner

    def position_to_coordinate(self, position: int) -> list[int]:
        return [position // self.size, position % self.size]

    def coordinate_to_position(self, coordinate: Sequence[int]) -> int:
        return coordinate[0] * self.size + coordinate[1]

    def get_valuable_moves(self, role: int, depth: int = 0, only_three: bool = False, only_four: bool = False) -> list[list[int]]:
        moves = self.evaluator.get_moves(role, depth, only_three, only_four)
        if not only_three and not only_four:
            center = self.size // 2
            if self.board[center][center] == 0 and [center, center] not in moves:
                moves.append([center, center])
        if not moves:
            return self._nearby_valid_moves() if not only_three and not only_four else []
        return moves[:20]

    def evaluate(self, role: int) -> int:
        winner = self.get_winner()
        if winner != 0:
            return FIVE * winner * role
        return self.evaluator.evaluate(role)

    def hash(self) -> int:
        return self.zobrist.current_hash

    def reverse(self) -> "Board":
        board = Board(self.size, -self.first_role)
        for move in self.history:
            board.put(move["i"], move["j"], -move["role"])
        return board

    def _count_in_direction(self, i: int, j: int, di: int, dj: int, role: int) -> int:
        count = 0
        while self._is_inside(i + di * count, j + dj * count):
            if self.board[i + di * count][j + dj * count] != role:
                break
            count += 1
        return count

    def _is_winning_move(self, i: int, j: int, role: int) -> bool:
        directions = ((1, 0), (0, 1), (1, 1), (1, -1))
        return any(
            self._count_in_direction(i, j, di, dj, role)
            + self._count_in_direction(i, j, -di, -dj, role)
            - 1
            >= 5
            for di, dj in directions
        )

    def _nearby_valid_moves(self) -> list[list[int]]:
        occupied = [(move["i"], move["j"]) for move in self.history]
        if not occupied:
            center = self.size // 2
            return [[center, center]]

        moves: set[tuple[int, int]] = set()
        for i, j in occupied[-6:]:
            for di in range(-2, 3):
                for dj in range(-2, 3):
                    ni = i + di
                    nj = j + dj
                    if self._is_inside(ni, nj) and self.board[ni][nj] == 0:
                        moves.add((ni, nj))
        return [[i, j] for i, j in sorted(moves)[:20]]

    def _is_inside(self, i: int, j: int) -> bool:
        return 0 <= i < self.size and 0 <= j < self.size
