from __future__ import annotations

from two_player_games.agent.human.board import BoardHuman
from two_player_games.model.board.horizontal import (
    HorizontalBoard,
    HorizontalBoardAction,
)


# TODO pylint: disable=too-few-public-methods
class HorizontalBoardHuman(BoardHuman[HorizontalBoardAction]):
    def select_action(
        self,
        model: HorizontalBoard,
    ) -> HorizontalBoardAction | None:
        if not model.possible_actions:
            return None
        self.view.human_action = None
        while self.view.human_action is None:
            # TODO Reintroduce mid-game event handling
            # event = self.view.get_event()
            self.view.get_event()
            # Ensure the cell is playable, otherwise reset it
            if (
                self.view.human_action is not None
                and self.view.human_action not in model.possible_actions
            ):
                self.view.human_action = None

            # TODO Reintroduce mid-game event handling
            # if event in {Event.QUIT, Event.RESTART}:
            #     return event
        return self.view.human_action
