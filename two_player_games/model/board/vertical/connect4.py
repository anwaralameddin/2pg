from __future__ import annotations

from functools import partial

import numpy as np
import numpy.typing as npt
from scipy.signal import convolve2d  # type: ignore

from two_player_games.common import MARK_EMPTY, Status, Turn
from two_player_games.config.board.connect4 import CONNECT4
from two_player_games.model import InvalidAction, PlayAfterGameOver
from two_player_games.model.board.vertical import (
    VerticalBoard,
    VerticalBoardAction,
)

FIRST_TURN = Turn.FIRST
SECOND_TURN = Turn.SECOND
FIRST_WON = Status.FIRST_WON
SECOND_WON = Status.SECOND_WON

ROW_NUM = CONNECT4.row_num
COL_NUM = CONNECT4.col_num

KERNEL_HORIZONTAL = np.array([[1, 1, 1, 1]], dtype=np.int8)
KERNEL_VERTICAL = np.array([[1], [1], [1], [1]], dtype=np.int8)
KERNEL_DIAGONAL = np.eye(4, dtype=np.int8)
KERNEL_DIAGONAL_FLIPLR = np.eye(4, dtype=np.int8)[:, ::-1]
WINNING_STREAK = 4


class Connect4(VerticalBoard):
    def __init__(self) -> None:
        super().__init__(ROW_NUM, COL_NUM)
        self._update_possible_actions()

    def _update_state_and_changes(self, action: VerticalBoardAction) -> None:
        count: int = (self.state[:, action] != MARK_EMPTY).sum(axis=0)
        change = ROW_NUM - 1 - count, action
        self.changes = [change]
        self.state[change] = self.turn.value

    def _update_scores(self, action: VerticalBoardAction | None) -> None:
        if action is None:
            self.scores[FIRST_TURN] = 0.5
            self.scores[SECOND_TURN] = 0.5
        elif self._is_won():
            if self.turn == FIRST_TURN:
                self.scores[FIRST_TURN] = 1
            else:
                self.scores[SECOND_TURN] = 1

    # TODO It would be more efficient to check only lines that contain the
    # last move
    def _is_won(self) -> bool:
        """Claclulate whether the executed move is a winning move."""
        cell_mark = self.turn.value
        state_eq_mark: npt.NDArray[np.bool_] = self.state == cell_mark
        horizontal: bool = (
            convolve2d(state_eq_mark, KERNEL_HORIZONTAL, mode="valid")
            == WINNING_STREAK
        ).any()
        vertical: bool = (
            convolve2d(state_eq_mark, KERNEL_VERTICAL, mode="valid")
            == WINNING_STREAK
        ).any()
        main_diagonal: bool = (
            convolve2d(state_eq_mark, KERNEL_DIAGONAL, mode="valid")
            == WINNING_STREAK
        ).any()
        anti_diagonal: bool = (
            convolve2d(state_eq_mark, KERNEL_DIAGONAL_FLIPLR, mode="valid")
            == WINNING_STREAK
        ).any()
        return horizontal or vertical or main_diagonal or anti_diagonal

    def _update_status(self, _action: VerticalBoardAction | None) -> None:
        match (self.scores[FIRST_TURN], self.scores[SECOND_TURN]):
            case (1, 0):
                self.status = FIRST_WON
            case (0, 1):
                self.status = SECOND_WON
            case (0.5, 0.5):
                self.status = Status.DRAW
            case _:
                pass
                # self.status = Status.RUNNING

    def _update_possible_actions(self) -> None:
        # TODO update more efficiently, e.g. by removing the last move
        self.possible_actions = [
            i
            for i, x in enumerate(
                (self.state == MARK_EMPTY).sum(axis=0) != 0,
            )
            if x
        ]

    # TODO Refactor: Move these repeated methods to Model
    # def deepcopy(self) -> Connect4:
    #     # FIXME Unclear why this is not working
    #     # return deepcopy(self)
    #     board = Connect4()
    #     board.changes = self.changes.copy()
    #     board.state = self.state.copy()
    #     board.turn = self.turn
    #     board.possible_actions = self.possible_actions.copy()
    #     board.scores = self.scores.copy()
    #     board.status = self.status
    #     return board

    # TODO Refactor: Move these repeated methods to Model
    def peek_then_eval(
        self,
        action: VerticalBoardAction,
        func: partial[tuple[float, VerticalBoardAction | None]],
    ) -> tuple[float, VerticalBoardAction | None]:
        # Save state
        changes = self.changes.copy()
        state = self.state.copy()
        turn = self.turn
        scores = self.scores.copy()
        status = self.status
        possible_actions = self.possible_actions.copy()

        # Execute
        if not self.is_over():
            if not self.play(action):
                raise InvalidAction(action, self.turn)
        else:
            # Unreachable
            raise PlayAfterGameOver(action)

        # Eval
        evaluation = func(self)

        # Undo execution
        self.changes = changes
        count = (self.state[:, action] != MARK_EMPTY).sum(axis=0)
        assert (
            count
        ), f"Column {action} must contain at least one non-empty cell."
        indices = ROW_NUM - count, action
        self.state[indices] = MARK_EMPTY
        self.scores = {
            FIRST_TURN: 0,
            SECOND_TURN: 0,
        }
        self.turn = turn
        self.status = status
        self._update_possible_actions()

        # TODO Move these assert statements to tests
        assert (
            changes == self.changes
        ), f"Grid not restored correctly\n{state}\n{self.state}"
        assert (
            state == self.state
        ).all(), f"Grid not restored correctly\n{state}\n{self.state}"
        assert (
            turn == self.turn
        ), f"Player turn not restored correctly\n{turn}\n{self.turn}"
        assert (
            scores == self.scores
        ), f"Scores not restored correctly\n{scores}\n{self.scores}"
        assert (
            possible_actions == self.possible_actions
        ), "Possible actions not restored correctly.\n{}\n{}".format(
            possible_actions,
            self.possible_actions,
        )
        assert (
            status == self.status
        ), f"Status not restored correctly\n{status}\n{self.status}"

        return evaluation
