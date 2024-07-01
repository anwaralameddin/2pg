from __future__ import annotations

from enum import StrEnum

from two_player_games.config import Config


class ModelArg(StrEnum):
    CONNECT4 = "connect4"
    OTHELLO = "othello"
    # PINOCHLE = "pinochle"
    # PONG = "pong"
    TICTACTOE = "tictactoe"

    # pylint: disable=import-outside-toplevel
    def get_model(self) -> type:
        match self:
            case ModelArg.CONNECT4:
                from .board.vertical.connect4 import Connect4

                return Connect4
            case ModelArg.OTHELLO:
                from .board.horizontal.othello import Othello

                return Othello
            case ModelArg.TICTACTOE:
                from .board.horizontal.tic_tac_toe import TicTacToe

                return TicTacToe

    # pylint: disable=import-outside-toplevel
    def get_config(self) -> Config:
        match self:
            case ModelArg.CONNECT4:
                from two_player_games.config.board.connect4 import CONNECT4

                return CONNECT4
            case ModelArg.OTHELLO:
                from two_player_games.config.board.othelo import OTHELO

                return OTHELO
            case ModelArg.TICTACTOE:
                from two_player_games.config.board.tic_tac_toe import TICTACTOE

                return TICTACTOE
