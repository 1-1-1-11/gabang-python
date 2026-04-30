from dataclasses import dataclass

from backend.app.board import Board
from backend.app.evaluation import FIVE
from backend.app.minmax import minmax, reset_search_cache, search_metrics


@dataclass(frozen=True)
class QualityCase:
    name: str
    size: int
    steps: tuple[tuple[int, int], ...]
    depth: int
    expected_moves: tuple[tuple[int, int], ...] | None
    min_value: int | None = None
    max_value: int | None = None
    max_nodes: int = 2_000
    max_candidate_moves: int = 5_000
    min_beta_cutoffs: int = 0
    expected_max_depth: int | None = None


QUALITY_CASES = (
    QualityCase(
        name="opening_center",
        size=9,
        steps=(),
        depth=3,
        expected_moves=((4, 4),),
        min_value=1,
        max_nodes=250,
        max_candidate_moves=600,
        min_beta_cutoffs=1,
        expected_max_depth=3,
    ),
    QualityCase(
        name="diagonal_immediate_win",
        size=6,
        steps=((0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 4)),
        depth=4,
        expected_moves=((4, 4),),
        min_value=FIVE,
        max_nodes=10,
        max_candidate_moves=10,
        min_beta_cutoffs=1,
        expected_max_depth=1,
    ),
    QualityCase(
        name="horizontal_must_block",
        size=7,
        steps=((2, 0), (2, 1), (6, 6), (2, 2), (5, 5), (2, 3), (4, 6), (2, 4)),
        depth=3,
        expected_moves=((2, 5),),
        max_value=0,
        max_nodes=800,
        max_candidate_moves=1_200,
        min_beta_cutoffs=1,
        expected_max_depth=4,
    ),
    QualityCase(
        name="simple_threat_sequence",
        size=9,
        steps=((4, 2), (0, 0), (4, 3), (0, 1), (4, 4), (0, 2)),
        depth=3,
        expected_moves=((4, 1), (4, 5)),
        min_value=1,
        max_nodes=120,
        max_candidate_moves=160,
        min_beta_cutoffs=1,
        expected_max_depth=3,
    ),
    QualityCase(
        name="midgame_search_budget",
        size=9,
        steps=((4, 4), (5, 3), (4, 5), (5, 4), (3, 5), (6, 4)),
        depth=3,
        expected_moves=None,
        min_value=1,
        max_nodes=2_000,
        max_candidate_moves=4_000,
        min_beta_cutoffs=100,
        expected_max_depth=4,
    ),
)


def play(board: Board, steps: tuple[tuple[int, int], ...]) -> None:
    for i, j in steps:
        assert board.put(i, j)


def metric_snapshot() -> dict[str, int]:
    return {key: search_metrics[key] for key in sorted(search_metrics)}


def run_quality_case(case: QualityCase):
    reset_search_cache()
    board = Board(size=case.size)
    play(board, case.steps)

    value, move, path = minmax(board, 1, depth=case.depth)

    return board, value, move, path, metric_snapshot()


def test_fixed_quality_positions_have_stable_moves_and_metrics():
    for case in QUALITY_CASES:
        board, value, move, path, metrics = run_quality_case(case)

        if case.expected_moves is not None:
            assert tuple(move) in case.expected_moves, case.name
        else:
            assert move in board.get_valid_moves(), case.name
        if case.min_value is not None:
            assert value >= case.min_value, case.name
        if case.max_value is not None:
            assert value <= case.max_value, case.name

        assert path[0] == move, case.name
        assert metrics["nodes"] > 0, case.name
        assert metrics["nodes"] <= case.max_nodes, case.name
        assert metrics["candidate_moves"] > 0, case.name
        assert metrics["candidate_moves"] <= case.max_candidate_moves, case.name
        assert metrics["leaf_nodes"] > 0, case.name
        assert metrics["cache_stores"] > 0, case.name
        assert metrics["beta_cutoffs"] >= case.min_beta_cutoffs, case.name
        if case.expected_max_depth is not None:
            assert metrics["max_depth"] == case.expected_max_depth, case.name


def test_midgame_quality_case_reuses_cache_on_repeated_search():
    case = next(case for case in QUALITY_CASES if case.name == "midgame_search_budget")
    board, first_value, first_move, first_path, _ = run_quality_case(case)

    second_value, second_move, second_path = minmax(board, 1, depth=case.depth)
    metrics = metric_snapshot()

    assert (second_value, second_move, second_path) == (first_value, first_move, first_path)
    assert metrics["cache_hits"] > 0
