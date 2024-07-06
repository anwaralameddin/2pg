from __future__ import annotations

import numpy as np
import pytest
from numpy.testing import assert_array_equal
from numpy.typing import NDArray
from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore

from two_player_games.agent.minimax.naive import MaxiMinNaive
from two_player_games.common import Turn
from two_player_games.config.board.tic_tac_toe import TICTACTOE
from two_player_games.model.board import BoardChange, BoardState
from two_player_games.model.board.horizontal import HorizontalBoardAction
from two_player_games.model.board.horizontal.tic_tac_toe import TicTacToe
from two_player_games.presenter import Presenter
from two_player_games.view.hidden import HiddenView

TICTACTOE_ARRAY = np.array(
    [
        [1, 1, -1],
        [-1, -1, 1],
        [1, -1, 1],
    ],
)

# TODO This test is too slow


def naive_maximin() -> NDArray[np.int8]:
    model = TicTacToe()
    config = TICTACTOE
    first_agent: MaxiMinNaive[
        HorizontalBoardAction,
        BoardState,
        BoardChange,
    ] = MaxiMinNaive(6, Turn.FIRST)
    second_agent: MaxiMinNaive[
        HorizontalBoardAction,
        BoardState,
        BoardChange,
    ] = MaxiMinNaive(6, Turn.SECOND)
    view: HiddenView[HorizontalBoardAction, BoardState, BoardChange] = (
        HiddenView(config)
    )
    presenter = Presenter(model, first_agent, second_agent, view, False)
    presenter.main_loop()
    return model.state


@pytest.mark.benchmark(group="maximin", disable_gc=True, warmup=False)
def test_naive_maximin(benchmark: BenchmarkFixture) -> None:
    result: NDArray[np.int8] = benchmark(naive_maximin)
    assert_array_equal(result, TICTACTOE_ARRAY)
