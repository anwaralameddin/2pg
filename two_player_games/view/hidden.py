from __future__ import annotations

import sys

from two_player_games.common import Event
from two_player_games.config.board import BoardConfig
from two_player_games.model import Action, Change, Model, State
from two_player_games.view import View


class HiddenView(View[Action, State, Change]):
    def __init__(self, config: BoardConfig) -> None:
        super().__init__(**config.__dict__)
        print(f"HiddenView: {config.title} ...\n")
        self.running = True
        self.human_action = None

    def get_event(self) -> Event:
        if self.running:
            # TODO Capture the key press event without blocking the program.
            # - Consider using the keyboard or crossbeams libraries
            return Event.NONE
        # TODO Capture the key press event instead of using the input function
        key = input()
        if key == "r":
            self.running = True
            return Event.RESTART
        if key == "q":
            return Event.QUIT
        self.display_menu_screen()
        return Event.NONE

    def update_state(
        self,
        model: Model[Action, State, Change],
    ) -> None:
        pass

    def update_scores(
        self,
        model: Model[Action, State, Change],
    ) -> None:
        pass

    def refresh(self) -> None:
        pass

    def restart(self) -> None:
        self.human_action = None

    def quit(self) -> None:
        sys.exit()

    def display_menu_screen(self) -> None:
        self.running = False
        print("\nPress r to restart the game and q to quit the game\n")

    # TODO Implement the display_help_screen method
    def display_help_screen(self) -> None:
        raise NotImplementedError(
            "Help screen is not yet implemented for the HiddenView.",
        )
