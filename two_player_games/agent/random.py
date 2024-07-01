from __future__ import annotations

import random

from two_player_games.agent import Agent
from two_player_games.model import Action, Change, Model, State


# TODO pylint: disable=too-few-public-methods
class Random(Agent[Action, State, Change]):
    def select_action(
        self,
        model: Model[Action, State, Change],
    ) -> Action | None:
        if not model.possible_actions:
            return None
        return random.choice(model.possible_actions)
