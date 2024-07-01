from __future__ import annotations

from two_player_games.common import Category

from . import BLACK, GREEN, WHITE, BoardConfig

OTHELO = BoardConfig(
    category=Category.HORIZONTAL_BOARD,
    title="Othello",
    row_num=8,
    col_num=8,
    screen_width=600,
    screen_height=600,
    corner_markers=[[2, 2], [2, 6], [6, 2], [6, 6]],
    bg_grid=GREEN,
    first_player_color=BLACK,
    second_player_color=WHITE,
    display_hint=True,
)
