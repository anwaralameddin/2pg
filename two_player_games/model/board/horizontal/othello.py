from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import partial

import numpy as np
import numpy.typing as npt

from two_player_games.common import (
    MARK_EMPTY,
    MARK_FIRST,
    MARK_SECOND,
    Status,
    Turn,
)
from two_player_games.config.board.othelo import OTHELO
from two_player_games.model import InvalidAction, PlayAfterGameOver
from two_player_games.model.board.horizontal import (
    HorizontalBoard,
    HorizontalBoardAction,
)

logger = logging.getLogger(__name__)

BLACK = Turn.FIRST
WHITE = Turn.SECOND
BLACK_MARK = MARK_FIRST
WHITE_MARK = MARK_SECOND
BLACK_WON = Status.FIRST_WON
WHITE_WON = Status.SECOND_WON

ROW_NUM = OTHELO.row_num
COL_NUM = OTHELO.col_num
INIT_BLACK = [
    (ROW_NUM // 2 - 1, COL_NUM // 2),
    (ROW_NUM // 2, COL_NUM // 2 - 1),
]
INIT_WHITE = [
    (ROW_NUM // 2 - 1, COL_NUM // 2 - 1),
    (ROW_NUM // 2, COL_NUM // 2),
]
GRID_INDICES = (
    np.array(list(np.ndindex(ROW_NUM, COL_NUM)))
    .view(
        dtype=np.dtype(
            [("row", "<i4"), ("column", "<i4")],
        ),
    )
    .reshape(ROW_NUM, COL_NUM)
)

DIRECTIONARRAY = (
    (np.array(list(np.ndindex(3, 3))) - 1)
    .view(
        dtype=np.dtype(
            [("row", "<i4"), ("column", "<i4")],
        ),
    )
    .reshape(9)
)

# FIXME Type inheritance is not correct here. Is this needed? Could it be a
# tuple, e.g. ((-1, -1),) , ...
DIRECTION = dict[str, tuple[int, int]](
    UP_LEFT=DIRECTIONARRAY[0],
    UP=DIRECTIONARRAY[1],
    UP_RIGHT=DIRECTIONARRAY[2],
    LEFT=DIRECTIONARRAY[3],
    CENTRE=DIRECTIONARRAY[4],
    RIGHT=DIRECTIONARRAY[5],
    DOWN_LEFT=DIRECTIONARRAY[6],
    DOWN=DIRECTIONARRAY[7],
    DOWN_RIGHT=DIRECTIONARRAY[8],
)


# TODO pylint: disable=too-many-instance-attributes
@dataclass
class Othello(HorizontalBoard):
    # Mark if the last turn was passed without playing
    _turn_passed: bool
    # The number of possible flips in each direction for each action.
    _possible_flips: dict[str, npt.NDArray[np.int8]]

    # TODO Avoid this repetition. This should be already covered in Model
    def __init__(self) -> None:
        super().__init__(ROW_NUM, COL_NUM)
        for cell in INIT_BLACK:
            self.changes.append(cell)
            self.state[cell] = BLACK_MARK
        for cell in INIT_WHITE:
            self.changes.append(cell)
            self.state[cell] = WHITE_MARK
        self.scores = {
            BLACK: len(INIT_BLACK),
            WHITE: len(INIT_WHITE),
        }
        self._turn_passed = False
        self._vectorized_possible_flips_per_direction = np.vectorize(
            self._possible_flips_per_direction,
            otypes=[int],
        )
        self.update_possible_actions()

    # TODO Refactor: Move these repeated methods to Model
    # TODO Consider overloading __init__ instead of deepcopy to avoid needing
    # to update protected attributes
    # def deepcopy(self) -> Othello:
    #     # FIXME Unclear why this is not working
    #     # return deepcopy(self)
    #     # metaclass=MultipleMeta
    #     board = Othello()
    #     board.changes = self.changes.copy()
    #     board.state = self.state.copy()
    #     board.turn = self.turn
    #     board.possible_actions = self.possible_actions.copy()
    #     board.scores = self.scores.copy()
    #     board.status = self.status
    #     # TODO pylint: disable=protected-access
    #     board._turn_passed = self._turn_passed
    #     board._possible_flips = self._possible_flips.copy()
    #     return board

    def _flip_and_update_score(
        self,
        action: HorizontalBoardAction,
        direction: tuple[int, int],
        count: int,
    ) -> None:
        """
        Flip the cells in the given direction starting from the one
        following the given action, updating scores accordingly.
        """
        cell_mark = self.turn.value
        # TODO Update more efficiently (without for loop)
        for _ in range(count):
            row = action[0] + direction[0]
            column = action[1] + direction[1]
            action = (row, column)
            self.changes.append(action)
            self.state[action] = cell_mark
        self.scores[self.turn] += count
        self.scores[-self.turn] -= count

    def _update_state_and_scores(self, action: HorizontalBoardAction) -> None:
        """Update the state and the scores when executing the given action."""
        self.state[action] = self.turn.value
        self.changes.append(action)
        self.scores[self.turn] += 1
        # TODO Update more efficiently (without for loop)
        for direction_name, direction_value in DIRECTION.items():
            self._flip_and_update_score(
                action,
                direction_value,
                self._possible_flips[direction_name][action],
            )

    def _update_status(self, action: HorizontalBoardAction | None) -> None:
        """Update the status when executing the given action."""
        if action is None:
            if self._turn_passed:
                # Game over
                # The game is over when both players pass consecutively
                if self.scores[BLACK] > self.scores[WHITE]:
                    self.status = BLACK_WON
                elif self.scores[BLACK] < self.scores[WHITE]:
                    self.status = WHITE_WON
                else:
                    self.status = Status.DRAW
            else:
                self._turn_passed = True
                self.changes = []
        else:
            self.status = Status.RUNNING
            self._turn_passed = False

    def _possible_flips_per_direction(
        self,
        action: HorizontalBoardAction,
        direction: tuple[int, int],
    ) -> int:
        """
        Return the number of possible flips in the given direction starting
        from the cell following the given action.
        """
        # TODO Is it more efficient to take slices and check possible flips for
        # each slice instead of the while loop?
        if self.state[action] != MARK_EMPTY:
            return 0
        result = 0
        player_cell = self.turn.value
        opponent_cell = -player_cell
        while True:
            row = action[0] + direction[0]
            column = action[1] + direction[1]
            action = (row, column)

            if not (0 <= row < self._row_num and 0 <= column < self._col_num):
                return 0
            if self.state[action] == player_cell:
                return result
            if self.state[action] == opponent_cell:
                result += 1
            else:
                # Empty cell
                return 0

    def _update_possible_flips(self) -> None:
        """Compute the possible flips for each cell in each direction."""
        self._possible_flips = {}
        for direction_name, direction_value in DIRECTION.items():
            self._possible_flips[direction_name] = (
                self._vectorized_possible_flips_per_direction(
                    GRID_INDICES,
                    direction_value,
                )
            )

    def update_possible_actions(self) -> None:
        """Compute possible actions, i.e. the cells that can be played."""
        self._update_possible_flips()
        self.possible_actions = [
            (row, column)
            for row in range(self._row_num)
            for column in range(self._col_num)
            if any(
                self._possible_flips[direction][(row, column)]
                for direction in DIRECTION
            )
        ]

    # TODO This implementation seems generic enough to be lifted up to Model
    def exec(self, action: HorizontalBoardAction | None) -> bool:
        # update_possible_actions() is always called before the next invocation
        # of exec(), so we can assume that possible_actions is up-to-date.
        if action is None:
            self._update_status(None)
        elif action not in self.possible_actions:
            return False
        else:
            self.changes = []
            self._update_state_and_scores(action)
            self._update_status(action)
        self.switch_turn()
        self.update_possible_actions()
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
        _turn_passed = self._turn_passed
        _possible_flips = {
            direction: self._possible_flips[direction][action]
            for direction in DIRECTION
        }

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
        # FIXME Look for a more efficient approach to restore the state
        self.changes = changes
        self.state[action] = MARK_EMPTY
        self.scores[turn] -= 1
        for direction_name, direction_value in DIRECTION.items():
            self._flip_and_update_score(
                action,
                direction_value,
                _possible_flips[direction_name],
            )
        self.turn = turn
        self.status = status
        self.update_possible_actions()
        self._turn_passed = _turn_passed

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
        assert (
            _turn_passed == self._turn_passed
        ), "turn_passed not restored correctly\n{}\n{}".format(
            _turn_passed,
            self._turn_passed,
        )
        assert _possible_flips == {
            direction: self._possible_flips[direction][action]
            for direction in DIRECTION
        }, "Possible flips not restored correctly.\n{}\n{}".format(
            _possible_flips,
            self._possible_flips,
        )

        return evaluation
