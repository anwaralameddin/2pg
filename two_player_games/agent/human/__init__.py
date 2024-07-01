from __future__ import annotations

from two_player_games.agent import Agent
from two_player_games.model import Action, Change, State
from two_player_games.view import View


# TODO pylint: disable=too-few-public-methods
class Human(Agent[Action, State, Change]):
    def __init__(self, view: View[Action, State, Change]) -> None:
        super().__init__()
        self.view = view
