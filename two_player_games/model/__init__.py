from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import partial
from typing import Generic, TypeVar

from two_player_games.common import Status, Turn

Action = TypeVar("Action")
State = TypeVar("State")
Change = TypeVar("Change")
# Item = TypeVar("Item")


@dataclass
class InvalidAction(Exception, Generic[Action]):
    action: Action
    turn: Turn

    def __str__(self) -> str:
        return f"Invalid action: {self.action} for turn: {self.turn}"


@dataclass
class PlayAfterGameOver(Exception, Generic[Action]):
    action: Action

    def __str__(self) -> str:
        return f"Attempted action after the game is over: {self.action}"


# pylint: disable=too-many-instance-attributes
class Model(ABC, Generic[Action, State, Change]):
    """
    An abstract class specifying the interface for a game model.

    It manages the game status and agents' interactions with the environment.
    """

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, value: State) -> None:
        self._state = value

    @property
    def changes(self) -> list[Change]:
        return self._changes

    @changes.setter
    def changes(self, value: list[Change]) -> None:
        self._changes = value

    @property
    def turn(self) -> Turn:
        return self._turn

    @turn.setter
    def turn(self, value: Turn) -> None:
        self._turn = value

    @property
    def possible_actions(self) -> list[Action]:
        """Return the possible actions for the current player."""
        return self._possible_actions

    @possible_actions.setter
    def possible_actions(self, value: list[Action]) -> None:
        """Set the possible actions for the current player."""
        self._possible_actions = value

    @property
    def scores(self) -> dict[Turn, float]:
        """Return the scores for each player."""
        return self._scores

    @scores.setter
    def scores(self, value: dict[Turn, float]) -> None:
        """Set the scores for each player."""
        self._scores = value

    @property
    def status(self) -> Status:
        """Return the game's status."""
        return self._status

    @status.setter
    def status(self, value: Status) -> None:
        """Set the game's status."""
        self._status = value

    @abstractmethod
    def __init__(self) -> None:
        self._turn = Turn.FIRST
        self._status = Status.RUNNING
        self.scores = {
            Turn.FIRST: 0,
            Turn.SECOND: 0,
        }
        """
        Subclasses must initialize the following attributes:
        - `self.state`
        - `self.changes`
        - `self._possible_actions`
        - model-specific attributes
        They also can override the following attributes:
        - `self._scores`
        Then, they must call the following method:
        - `self._update_possible_actions()`
        """

    def play(self, action: Action | None) -> bool:
        """
        Execute the given action.

        The method returns True if executed successfully; otherwise, False.
        """
        if action is None:
            self.changes = []
        elif action not in self.possible_actions:
            return False
        else:
            self._update_state_and_changes(action)
        self._update_scores(action)
        self._update_status(action)
        self._switch_turn()
        self._update_possible_actions()
        return True

    @abstractmethod
    def _update_state_and_changes(self, action: Action) -> None:
        """Update state and changes for the given action."""
        # No need to check for invalid actions as this method is only called
        # for actions in self.possible_actions

    @abstractmethod
    def _update_scores(self, action: Action | None) -> None:
        """Update scores for each player for the given action."""

    @abstractmethod
    def _update_status(self, action: Action | None) -> None:
        """Update the status for the given action."""

    def _switch_turn(self) -> None:
        """Switch the current player."""
        self.turn = -self.turn

    @abstractmethod
    def _update_possible_actions(self) -> None:
        """Update the possible actions for the current player."""

    def restart(self) -> None:
        # FIXME Refactor board and othello to help avoid using __init__
        # pylint: disable=unnecessary-dunder-call
        self.__init__()  # type: ignore

    def reward(self, turn: Turn) -> float:
        """Return the reward for the given player."""
        return self.scores[turn] - self.scores[-turn]

    def is_over(self) -> bool:
        return self.status != Status.RUNNING

    @abstractmethod
    def peek_then_eval(
        self,
        action: Action,
        func: partial[tuple[float, Action | None]],
    ) -> tuple[float, Action | None]:
        """
        Execute, evaluate, and undo the given action.

        This entails:
        1 - Executing the given action
        2 - Evaluating the given function on the new state
        3 - Undoing the execution,
        3 - Returning the evaluation.
        """
