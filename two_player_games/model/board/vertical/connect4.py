from __future__ import annotations

import logging
from functools import partial

import numpy as np
from scipy.signal import convolve2d

from two_player_games.common import MARK_EMPTY, Status, Turn
from two_player_games.config.board.connect4 import CONNECT4
from two_player_games.model import InvalidAction, PlayAfterGameOver
from two_player_games.model.board.vertical import (
    VerticalBoard,
    VerticalBoardAction,
)

logger = logging.getLogger(__name__)

FIRST_TURN = Turn.FIRST
SECOND_TURN = Turn.SECOND
# FIRST_MARK = MARK_FIRST
# SECOND_MARK = MARK_SECOND
FIRST_WON = Status.FIRST_WON
SECOND_WON = Status.SECOND_WON

ROW_NUM = CONNECT4.row_num
COL_NUM = CONNECT4.col_num

KERNEL_HORIZONTAL = np.array([[1, 1, 1, 1]])
KERNEL_VERTICAL = np.array([[1], [1], [1], [1]])
KERNEL_DIAGONAL = np.eye(4)
KERNEL_DIAGONAL_REVERSE = np.eye(4)[:, ::-1]
WINNING_STREAK = 4


class Connect4(VerticalBoard):
    def __init__(self) -> None:
        super().__init__(ROW_NUM, COL_NUM)
        self.scores = {
            FIRST_TURN: 0,
            SECOND_TURN: 0,
        }
        self.update_possible_actions()

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

    def _update_status_and_scores(self) -> None:
        """Update the status and the scores during action execution."""
        if self._is_winning():
            if self.turn == FIRST_TURN:
                self.status = FIRST_WON
                self.scores[FIRST_TURN] += 1
            else:
                self.status = SECOND_WON
                self.scores[SECOND_TURN] += 1
        elif not self.possible_actions:
            self.status = Status.DRAW
            self.scores[FIRST_TURN] += 0.5
            self.scores[SECOND_TURN] += 0.5

    # TODO It would be more efficient to check only lines that contain the
    # last move
    def _is_winning(self) -> bool:
        """Claclulate whether the executed move is a winning move."""
        cell_mark = self.turn.value
        state_eq_mark = self.state == cell_mark
        horizontal: bool = (
            convolve2d(state_eq_mark, KERNEL_HORIZONTAL, mode="valid")
            == WINNING_STREAK
        ).any()
        vertical: bool = (
            convolve2d(state_eq_mark, KERNEL_VERTICAL, mode="valid")
            == WINNING_STREAK
        ).any()
        diagonal: bool = (
            convolve2d(state_eq_mark, KERNEL_DIAGONAL, mode="valid")
            == WINNING_STREAK
        ).any()
        diagonal_reverse: bool = (
            convolve2d(state_eq_mark, KERNEL_DIAGONAL_REVERSE, mode="valid")
            == WINNING_STREAK
        ).any()

        return horizontal or vertical or diagonal or diagonal_reverse

    # TODO Implement more efficiently
    def update_possible_actions(self) -> None:
        """Update possible actions, i.e. the columns that can be played."""
        self.possible_actions = [
            i
            for i, x in enumerate(
                (self.state != MARK_EMPTY).sum(axis=0) != ROW_NUM,
            )
            if x
        ]

    def exec(self, action: VerticalBoardAction | None) -> bool:
        # update_possible_actions() is always called before the next invocation
        # of exec(), so we can assume that possible_actions is up-to-date.
        # Different from Othello, action can only be none when the game is over
        if action is not None:
            if action not in self.possible_actions:
                return False
            count: int = (self.state[:, action] != MARK_EMPTY).sum(axis=0)
            indices = ROW_NUM - 1 - count, action
            self.changes = [indices]
            self.state[indices] = self.turn.value
        self.update_possible_actions()
        self._update_status_and_scores()
        self.switch_turn()
        return True

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
            if not self.exec(action):
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
        self.update_possible_actions()

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
