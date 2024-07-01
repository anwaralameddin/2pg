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
        """
        Subclasses should initialize the following attributes:
        - self.state
        - self.changes
        - self._possible_actions
        - self._scores
        """

    def restart(self) -> None:
        # FIXME Refactor board and othello to help avoid using __init__
        # pylint: disable=unnecessary-dunder-call
        self.__init__()  # type: ignore

    def reward(self, turn: Turn) -> float:
        """Return the reward for the given player."""
        return self.scores[turn] - self.scores[-turn]

    def switch_turn(self) -> None:
        self.turn = -self.turn

    def is_over(self) -> bool:
        return self.status != Status.RUNNING

    @abstractmethod
    def update_possible_actions(self) -> None:
        pass

    @abstractmethod
    def exec(self, action: Action | None) -> bool:
        """
        Execute the given action.

        The method returns True if executed successfully; otherwise, False.

        This entails:
        - Updating the state and the scores
        - Updating the status
        - Switching the turn
        - Updating possible actions
        """

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
