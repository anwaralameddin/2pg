from __future__ import annotations

from two_player_games.common import RGB, Category
from two_player_games.config import Config

BLACK: RGB = (0, 0, 0)
BLUE: RGB = (0, 100, 150)
GRAY: RGB = (127, 127, 127)
GREEN: RGB = (0, 150, 100)
PINK: RGB = (255, 100, 150)
RED: RGB = (255, 0, 0)
WHITE: RGB = (255, 255, 255)
YELLOW: RGB = (255, 255, 0)


# TODO Revert back to using data classes
# TODO pylint: disable=too-many-instance-attributes,too-few-public-methods
class BoardConfig(Config):
    # TODO pylint: disable=too-many-arguments,too-many-locals
    def __init__(
        self,
        title: str,
        row_num: int,
        col_num: int,
        screen_width: int,
        screen_height: int,
        corner_markers: list[list[int]],
        bg_grid: RGB,
        category: Category = Category.BOARD,
        first_player_color: RGB = BLACK,
        second_player_color: RGB = WHITE,
        game_over_color: RGB = RED,
        bg_scores_pane: RGB = GRAY,
        fg_line: RGB = BLACK,
        bg_draw: RGB = GRAY,
        text_hight: int = 50,
        padding: int = 5,
        line_thickness: int = 2,
        font_family: str = "Arial",
        font_size: int = 30,
        hint_num: int = 3,
        display_hint: bool = False,
    ) -> None:
        super().__init__(category)
        self.title = title
        self.row_num = row_num
        self.col_num = col_num
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.corner_markers = corner_markers
        self.bg_grid = bg_grid
        self.first_player_color = first_player_color
        self.second_player_color = second_player_color
        self.game_over_color = game_over_color
        self.bg_scores_pane = bg_scores_pane
        self.fg_line = fg_line
        self.bg_draw = bg_draw
        self.text_hight = text_hight
        self.padding = padding
        self.line_thickness = line_thickness
        self.font_family = font_family
        self.font_size = font_size
        self.hint_num = hint_num
        self.display_hint = display_hint
