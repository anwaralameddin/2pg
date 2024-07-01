from __future__ import annotations

from two_player_games.common import Category
from two_player_games.config.board import BoardConfig
from two_player_games.model import Action
from two_player_games.model.board import BoardChange, BoardState
from two_player_games.view import View
from two_player_games.view.pygame.board import PyGameBoardView


class PyGameView(View[Action, BoardState, BoardChange]):
    def __new__(
        cls,
        config: BoardConfig,
    ) -> PyGameView[Action]:
        match config.category:
            case Category.VERTICAL_BOARD | Category.HORIZONTAL_BOARD:
                return PyGameBoardView(config)
            case _:
                raise ValueError(f"Unsupported category: {config.category}")
