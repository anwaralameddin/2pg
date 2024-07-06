from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Generic

from two_player_games.agent import Agent
from two_player_games.common import Event, Turn
from two_player_games.model import Action, Change, InvalidAction, Model, State
from two_player_games.view import View

logger = logging.getLogger(__name__)


@dataclass
class Presenter(Generic[Action, State, Change]):
    model: Model[Action, State, Change]
    first_agent: Agent[Action, State, Change]
    second_agent: Agent[Action, State, Change]
    view: View[Action, State, Change]

    def restart(self) -> None:
        self.model.restart()
        self.view.restart()
        self.main_loop()

    def quit(self) -> None:
        self.view.quit()

    def main_loop(self) -> None:
        while not self.model.is_over():
            logger.debug(
                "Changes: %s",
                self.model.changes,
            )
            self.view.update(self.model)
            event = self.view.get_event()
            if event == Event.QUIT:
                return
            current_agent = (
                self.first_agent
                if self.model.turn == Turn.FIRST
                else self.second_agent
            )
            action = current_agent.select_action(self.model)
            # TODO Separate the action selection from event handling
            # This approach is mostly relevant to the human agent
            match action:
                case Event.QUIT:
                    self.quit()
                    return
                case Event.RESTART:
                    self.restart()
                    return
                case Event.NONE:
                    pass
                case Event.MENU | Event.HELP | Event.CLICKED:
                    # TODO Explain why did you include CLICKED here
                    raise NotImplementedError(
                        "Menu and help are not implemented.",
                    )
                case _:
                    logger.debug(
                        "%s: %s",
                        self.model.turn,
                        action,
                    )
                    if not self.model.play(action):
                        raise InvalidAction(action, self.model.turn)
            # TODO `cell` is board specific. Replace it with a more generic
            # property or method
            self.view.human_action = None
        logger.debug(
            "Changes: %s",
            self.model.changes,
        )
        self.view.update(self.model)

        logger.info(
            "Game over (%s): %s",
            self.model.status.name,
            self.model.scores,
        )

        self.menu_loop()

    def menu_loop(self) -> None:
        self.view.display_menu_screen()

        while True:
            event = self.view.get_event()
            match event:
                case Event.QUIT:
                    self.quit()
                    break
                case Event.RESTART:
                    self.restart()
                    break
                case Event.MENU | Event.NONE | Event.CLICKED:
                    # TODO Remove CLICKED from here when implemented
                    pass
                case Event.HELP:
                    self.help_loop()
                    break

    def help_loop(self) -> None:
        self.view.display_help_screen()

        while True:
            event = self.view.get_event()
            match event:
                case Event.QUIT:
                    self.quit()
                    break
                case Event.RESTART:
                    self.restart()
                    break
                case Event.MENU:
                    self.menu_loop()
                    break
                case Event.HELP | Event.NONE | Event.CLICKED:
                    # TODO Remove CLICKED from here when implemented
                    pass
