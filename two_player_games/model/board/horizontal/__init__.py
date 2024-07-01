from __future__ import annotations

from two_player_games.model.board import Board

HorizontalBoardAction = tuple[int, int]
HorizontalBoard = Board[HorizontalBoardAction]
