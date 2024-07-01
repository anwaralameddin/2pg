from __future__ import annotations

import random
import sys
from abc import abstractmethod

from two_player_games.agent import Agent
from two_player_games.common import Turn
from two_player_games.model import Action, Change, Model, State


class MaxiMin(Agent[Action, State, Change]):
    def __init__(self, depth: int, maximin_turn: Turn) -> None:
        super().__init__()
        if depth <= 0:
            print("Minmax depth must be greater than 0.", file=sys.stderr)
            sys.exit(1)
        self.depth = depth
        self.maximin_turn = maximin_turn

    @abstractmethod
    def maximin(
        self,
        model: Model[Action, State, Change],
        depth: int,
        turn: Turn,
    ) -> tuple[float, Action | None]:
        pass

    def select_action(
        self,
        model: Model[Action, State, Change],
    ) -> Action | None:
        _, action = self.maximin(model, self.depth, self.maximin_turn)
        if model.possible_actions and action is None:
            action = random.choice(model.possible_actions)
        return action
