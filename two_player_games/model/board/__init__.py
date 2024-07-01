from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

import numpy as np

from two_player_games.common import CellMark
from two_player_games.model import Action, Model

# Piece = TypeVar("Piece")


# pylint: disable=unsubscriptable-object
BoardState = np.ndarray[Any, Any]
BoardChange = tuple[int, int]


@dataclass
class Board(
    Model[Action, BoardState, BoardChange],
):
    _row_num: int
    _col_num: int

    @abstractmethod
    def __init__(self, row_num: int, col_num: int) -> None:
        super().__init__()

        # FIXME Avoid this repetition. This should be already covered in Model
        self.state = np.zeros((row_num, col_num), CellMark)
        self.changes = []
        self._row_num = row_num
        self._col_num = col_num
