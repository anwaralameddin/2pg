from __future__ import annotations

from enum import StrEnum


class ViewArg(StrEnum):
    HIDDEN = "hidden"
    PYGAME = "pygame"
    # TERMINAL = "terminal"

    # pylint: disable=import-outside-toplevel
    def get_view(self) -> type:
        match self:
            case ViewArg.HIDDEN:
                from .hidden import HiddenView

                return HiddenView
            case ViewArg.PYGAME:
                from .pygame import PyGameView

                return PyGameView
