from __future__ import annotations

from enum import Enum, Flag, auto


class Category(Flag):
    HORIZONTAL_BOARD = auto()
    VERTICAL_BOARD = auto()
    BOARD = HORIZONTAL_BOARD | VERTICAL_BOARD
    # Cards = auto()


class Status(Enum):  # Status(Flag)
    RUNNING = auto()
    FIRST_WON = auto()
    SECOND_WON = auto()
    DRAW = auto()
    # GAME_OVER = FIRST_WON | SECOND_WON | DRAW


class Event(Enum):
    NONE = auto()
    CLICKED = auto()
    QUIT = "q"
    RESTART = "r"
    MENU = "m"
    HELP = "h"


# Enum is avoided here for its effect on the performance
# TODO What about other instances of Enum?
CellMark = int
MARK_EMPTY = CellMark(0)
MARK_FIRST = CellMark(1)
MARK_SECOND = CellMark(-1)


class Turn(Enum):
    FIRST = MARK_FIRST
    SECOND = MARK_SECOND

    def __neg__(self) -> Turn:
        return Turn.FIRST if self == Turn.SECOND else Turn.SECOND


RGB = tuple[int, int, int]
