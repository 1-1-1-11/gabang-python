from backend.app.shape import DIRECTIONS, Shape, get_shape_fast

FIVE = 10_000_000
BLOCK_FIVE = FIVE
FOUR = 100_000
FOUR_FOUR = FOUR
FOUR_THREE = FOUR
THREE_THREE = FOUR // 2
BLOCK_FOUR = 1_500
THREE = 1_000
BLOCK_THREE = 150
TWO_TWO = 200
TWO = 100
ONE = 10

# Scores for an empty candidate point before the piece is placed. Terminal
# winner scores are handled by Board.evaluate(), matching the original JS split.
CANDIDATE_SHAPE_SCORE = {
    Shape.FIVE: FOUR,
    Shape.BLOCK_FIVE: BLOCK_FOUR,
    Shape.FOUR: THREE,
    Shape.BLOCK_FOUR: BLOCK_THREE,
    Shape.THREE: TWO,
    Shape.BLOCK_THREE: 15,
    Shape.TWO: ONE,
}


class Evaluate:
    def __init__(self, size: int = 15):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.history: list[tuple[int, int, int]] = []

    def move(self, i: int, j: int, role: int) -> None:
        self.board[i][j] = role
        self.history.append((i, j, role))

    def undo(self, i: int, j: int) -> None:
        self.board[i][j] = 0
        if self.history:
            self.history.pop()

    def evaluate(self, role: int) -> int:
        return self._role_score(role) - self._role_score(-role)

    def get_moves(self, role: int, depth: int = 0, only_three: bool = False, only_four: bool = False) -> list[list[int]]:
        groups = self._point_groups(role)
        fives = groups[Shape.FIVE] | groups[Shape.BLOCK_FIVE]
        if fives:
            return self._to_coordinates(fives)

        fours = groups[Shape.FOUR]
        block_fours = groups[Shape.BLOCK_FOUR]
        if only_four or fours:
            return self._to_coordinates(fours | block_fours)

        four_fours = groups[Shape.FOUR_FOUR]
        if four_fours:
            return self._to_coordinates(four_fours | block_fours)

        four_threes = groups[Shape.FOUR_THREE]
        threes = groups[Shape.THREE]
        if four_threes:
            return self._to_coordinates(four_threes | block_fours | threes)

        three_threes = groups[Shape.THREE_THREE]
        if three_threes:
            return self._to_coordinates(three_threes | block_fours | threes)

        if only_three:
            return self._to_coordinates(block_fours | threes)

        candidates = block_fours | threes | groups[Shape.BLOCK_THREE] | groups[Shape.TWO_TWO] | groups[Shape.TWO]
        return self._to_coordinates(set(sorted(candidates)[:20]) if candidates else set())

    def _role_score(self, role: int) -> int:
        score = 0
        for point in self._candidate_points():
            i = point // self.size
            j = point % self.size
            shapes = self._shapes_at(i, j, role)
            for shape in shapes:
                score += CANDIDATE_SHAPE_SCORE.get(shape, 0)
            if shapes.count(Shape.BLOCK_FOUR) >= 2:
                score += CANDIDATE_SHAPE_SCORE[Shape.FOUR]
            if Shape.BLOCK_FOUR in shapes and Shape.THREE in shapes:
                score += CANDIDATE_SHAPE_SCORE[Shape.FOUR]
            if shapes.count(Shape.THREE) >= 2:
                score += THREE_THREE // 10
            if shapes.count(Shape.TWO) >= 2:
                score += TWO_TWO // 10
        return score

    def _point_groups(self, role: int) -> dict[Shape, set[int]]:
        groups = {shape: set() for shape in Shape}
        candidates = self._candidate_points()
        for r in (role, -role):
            for point in candidates:
                i = point // self.size
                j = point % self.size
                shapes = self._shapes_at(i, j, r)
                for shape in shapes:
                    if shape != Shape.NONE:
                        groups[shape].add(point)
                if shapes.count(Shape.BLOCK_FOUR) >= 2:
                    groups[Shape.FOUR_FOUR].add(point)
                if Shape.BLOCK_FOUR in shapes and Shape.THREE in shapes:
                    groups[Shape.FOUR_THREE].add(point)
                if shapes.count(Shape.THREE) >= 2:
                    groups[Shape.THREE_THREE].add(point)
                if shapes.count(Shape.TWO) >= 2:
                    groups[Shape.TWO_TWO].add(point)
        return groups

    def _shapes_at(self, i: int, j: int, role: int) -> list[Shape]:
        return [get_shape_fast(self.board, i, j, di, dj, role)[0] for di, dj in DIRECTIONS]

    def _candidate_points(self, radius: int = 2) -> list[int]:
        if not self.history:
            center = self.size // 2
            return [center * self.size + center]

        points: set[int] = set()
        for i, j, _ in self.history:
            for di in range(-radius, radius + 1):
                for dj in range(-radius, radius + 1):
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < self.size and 0 <= nj < self.size and self.board[ni][nj] == 0:
                        points.add(ni * self.size + nj)
        return sorted(points)

    def _to_coordinates(self, points: set[int]) -> list[list[int]]:
        return [[point // self.size, point % self.size] for point in sorted(points)]
