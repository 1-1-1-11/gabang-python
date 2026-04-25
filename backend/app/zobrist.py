import random


class Zobrist:
    def __init__(self, size: int, seed: int = 20231123):
        self.size = size
        rng = random.Random(seed)
        self.table = [
            [{1: rng.getrandbits(64), -1: rng.getrandbits(64)} for _ in range(size)]
            for _ in range(size)
        ]
        self.current_hash = 0

    def toggle_piece(self, i: int, j: int, role: int) -> None:
        self.current_hash ^= self.table[i][j][role]
