from __future__ import annotations

from functools import partial

import numpy as np
import numpy.typing as npt

from two_player_games.common import MARK_EMPTY, Status, Turn
from two_player_games.config.board.tic_tac_toe import TICTACTOE
from two_player_games.model import InvalidAction, PlayAfterGameOver
from two_player_games.model.board.horizontal import (
    HorizontalBoard,
    HorizontalBoardAction,
)

X_TURN = Turn.FIRST
O_TURN = Turn.SECOND
X_WON = Status.FIRST_WON
O_WON = Status.SECOND_WON

ROW_NUM = TICTACTOE.row_num
COL_NUM = TICTACTOE.col_num


class TicTacToe(HorizontalBoard):
    def __init__(self) -> None:
        super().__init__(ROW_NUM, COL_NUM)
        self._update_possible_actions()

    def _update_state_and_changes(self, action: HorizontalBoardAction) -> None:
        self.changes = [action]
        self.state[action] = self.turn.value

    def _update_scores(self, action: HorizontalBoardAction | None) -> None:
        if action is None:
            self.scores[X_TURN] = 0.5
            self.scores[O_TURN] = 0.5
        elif self._is_won():
            if self.turn == X_TURN:
                self.scores[X_TURN] = 1
            else:
                self.scores[O_TURN] = 1

    # TODO It would be more efficient to check only lines that contain the
    # last move
    def _is_won(self) -> bool:
        """Claclulate whether the executed move is a winning move."""
        cell_mark = self.turn.value
        # TODO Compare the performance of the following with an approach using
        # convolutions, similar to Connect4
        state_eq_mark: npt.NDArray[np.bool_] = self.state == cell_mark
        vertical: bool = state_eq_mark.all(axis=0).any()
        horizontal: bool = state_eq_mark.all(axis=1).any()
        diagonal: bool = (np.diag(self.state) == cell_mark).all() or (
            np.diag(self.state[:, ::-1]) == cell_mark
        ).all()
        return vertical or horizontal or diagonal

    def _update_status(self, _action: HorizontalBoardAction | None) -> None:
        match (self.scores[X_TURN], self.scores[O_TURN]):
            case (1, 0):
                self.status = X_WON
            case (0, 1):
                self.status = O_WON
            case (0.5, 0.5):
                self.status = Status.DRAW
            case _:
                pass
                # self.status = Status.RUNNING

    def _update_possible_actions(self) -> None:
        # TODO update more efficiently, e.g. by removing the last move
        self.possible_actions = [
            (row, col)
            for row in range(self._row_num)
            for col in range(self._col_num)
            if self.state[row, col] == MARK_EMPTY
        ]

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
            if not self.play(action):
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
