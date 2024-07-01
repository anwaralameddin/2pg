from __future__ import annotations

from two_player_games.common import Category

from . import BLACK, BLUE, PINK, RED, YELLOW, BoardConfig

CONNECT4 = BoardConfig(
    category=Category.VERTICAL_BOARD,
    title="Connect Four",
    row_num=6,
    col_num=7,
    screen_width=700,
    screen_height=600,
    corner_markers=[],
    bg_grid=BLUE,
    first_player_color=YELLOW,
    second_player_color=RED,
    game_over_color=BLUE,
    bg_scores_pane=BLACK,
    bg_draw=PINK,
)
