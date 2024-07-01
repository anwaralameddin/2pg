from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic

from two_player_games.common import RGB, Category, Event
from two_player_games.model import Action, Change, Model, State


# TODO pylint: disable=too-many-instance-attributes
@dataclass
class View(ABC, Generic[Action, State, Change]):
    category: Category
    title: str
    row_num: int
    col_num: int
    screen_width: int
    screen_height: int
    corner_markers: list[list[int]]
    bg_grid: RGB
    first_player_color: RGB
    second_player_color: RGB
    game_over_color: RGB
    fg_line: RGB
    bg_draw: RGB
    bg_scores_pane: RGB
    text_hight: int
    padding: int
    line_thickness: int
    font_family: str
    font_size: int
    hint_num: int
    display_hint: bool

    @abstractmethod
    def get_event(self) -> Event:
        pass

    @abstractmethod
    def update_state(
        self,
        model: Model[Action, State, Change],
    ) -> None:
        pass

    @abstractmethod
    def update_scores(
        self,
        model: Model[Action, State, Change],
    ) -> None:
        pass

    @abstractmethod
    def refresh(self) -> None:
        pass

    def update(
        self,
        model: Model[Action, State, Change],
    ) -> None:
        self.update_state(model)
        self.update_scores(model)
        self.refresh()

    # TODO Implement the display_menu_screen method
    @abstractmethod
    def display_menu_screen(self) -> None:
        pass

    # TODO Implement the display_help_screen method
    @abstractmethod
    def display_help_screen(self) -> None:
        pass

    @abstractmethod
    def restart(self) -> None:
        pass

    @abstractmethod
    def quit(self) -> None:
        pass

    @property
    def human_action(self) -> Action | None:
        return self._human_action

    @human_action.setter
    def human_action(self, human_action: Action | None) -> None:
        self._human_action = human_action
