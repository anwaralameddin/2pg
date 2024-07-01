from __future__ import annotations

from two_player_games.agent.human import Human
from two_player_games.model import Action
from two_player_games.model.board import BoardChange, BoardState

BoardHuman = Human[Action, BoardState, BoardChange]
