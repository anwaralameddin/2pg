from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic

from two_player_games.model import Action, Change, Model, State


# TODO Replace the agent class with a function signature, as it only utilises
# too few public methods.
# TODO pylint: disable=too-few-public-methods
class Agent(ABC, Generic[Action, State, Change]):
    """An abstract class specifying the agent interface."""

    @abstractmethod
    def select_action(
        self,
        model: Model[Action, State, Change],
    ) -> Action | None:
        pass
        # TODO If the view emits an event, it should be returned instead.
        # Currently, the view does not close before the game is over. This
        # change would allow the user to interrupt the game.
