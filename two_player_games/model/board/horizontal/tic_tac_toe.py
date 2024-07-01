from __future__ import annotations

import logging
from functools import partial

import numpy as np

from two_player_games.common import MARK_EMPTY, Status, Turn
from two_player_games.config.board.tic_tac_toe import TICTACTOE
from two_player_games.model import InvalidAction, PlayAfterGameOver
from two_player_games.model.board.horizontal import (
    HorizontalBoard,
    HorizontalBoardAction,
)

logger = logging.getLogger(__name__)

X_TURN = Turn.FIRST
O_TURN = Turn.SECOND
# X_MARK = MARK_FIRST
# O_MARK = MARK_SECOND
X_WON = Status.FIRST_WON
O_WON = Status.SECOND_WON

ROW_NUM = TICTACTOE.row_num
COL_NUM = TICTACTOE.col_num


class TicTacToe(HorizontalBoard):
    def __init__(self) -> None:
        super().__init__(ROW_NUM, COL_NUM)
        self.scores = {
            X_TURN: 0,
            O_TURN: 0,
        }
        self.update_possible_actions()

    # TODO Refactor: Move these repeated methods to Model
    # def deepcopy(self) -> TicTacToe:
    #     # FIXME Unclear why this is not working
    #     # return deepcopy(self)
    #     board = TicTacToe()
    #     board.changes = self.changes.copy()
    #     board.state = self.state.copy()
    #     board.turn = self.turn
    #     board.possible_actions = self.possible_actions.copy()
    #     board.scores = self.scores.copy()
    #     board.status = self.status
    #     return board

    def _update_status_and_scores(self) -> None:
        """Update the status and the scores during execution."""
        if self._is_winning():
            if self.turn == X_TURN:
                self.status = X_WON
                self.scores[X_TURN] += 1
            else:
                self.status = O_WON
                self.scores[O_TURN] += 1
        elif not self.possible_actions:
            self.status = Status.DRAW
            self.scores[X_TURN] += 0.5
            self.scores[O_TURN] += 0.5

    # TODO It would be more efficient to check only lines that contain the
    # last move
    def _is_winning(self) -> bool:
        """Claclulate whether the executed move is a winning move."""
        cell_mark = self.turn.value
        state_eq_mark = self.state == cell_mark
        # TODO Compare the performance of the following with an approach using
        # convolutions, similar to Connect4
        vertical = state_eq_mark.all(axis=0).any()
        horizontal = state_eq_mark.all(axis=1).any()
        diagonal = (np.diag(self.state) == cell_mark).all() or (
            np.diag(np.fliplr(self.state)) == cell_mark
        ).all()
        return bool(vertical or horizontal or diagonal)

    def update_possible_actions(self) -> None:
        """Update possible actions, i.e. the cells that can be played."""
        self.possible_actions = [
            (row, col)
            for row in range(self._row_num)
            for col in range(self._col_num)
            if self.state[row, col] == MARK_EMPTY
        ]

    def exec(self, action: HorizontalBoardAction | None) -> bool:
        # update_possible_actions() is always called before the next invocation
        # of exec(), so we can assume that possible_actions is up-to-date.
        # Different from Othello, action can only be none when the game is over
        if action is not None:
            if action not in self.possible_actions:
                return False
            self.changes = [action]
            self.state[action] = self.turn.value
        self.update_possible_actions()
        self._update_status_and_scores()
        self.switch_turn()
        return True

    # TODO Refactor: Move these repeated methods to Model
    def peek_then_eval(
        self,
        action: HorizontalBoardAction,
        func: partial[tuple[float, HorizontalBoardAction | None]],
    ) -> tuple[float, HorizontalBoardAction | None]:
        # TODO Why not use deep copy? Benchmark both options
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
        self.state[action] = MARK_EMPTY
        self.scores = {
            X_TURN: 0,
            O_TURN: 0,
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
