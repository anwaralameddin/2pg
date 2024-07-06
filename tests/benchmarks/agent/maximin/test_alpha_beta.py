from __future__ import annotations

import numpy as np
import pytest
from numpy.testing import assert_array_equal
from numpy.typing import NDArray
from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore

from two_player_games.agent.minimax.alpha_beta_pruning import AlphaBetaPruning
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


def alpha_beta_pruning() -> NDArray[np.int8]:
    model = TicTacToe()
    config = TICTACTOE
    first_agent: AlphaBetaPruning[
        HorizontalBoardAction,
        BoardState,
        BoardChange,
    ] = AlphaBetaPruning(6, Turn.FIRST)
    second_agent: AlphaBetaPruning[
        HorizontalBoardAction,
        BoardState,
        BoardChange,
    ] = AlphaBetaPruning(6, Turn.SECOND)
    view: HiddenView[HorizontalBoardAction, BoardState, BoardChange] = (
        HiddenView(config)
    )
    presenter = Presenter(model, first_agent, second_agent, view, False)
    presenter.main_loop()
    return model.state


@pytest.mark.benchmark(group="maximin", disable_gc=True, warmup=False)
def test_alpha_beta_pruning(benchmark: BenchmarkFixture) -> None:
    result: NDArray[np.int8] = benchmark(alpha_beta_pruning)
    assert_array_equal(result, TICTACTOE_ARRAY)
