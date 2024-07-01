from __future__ import annotations

from two_player_games.common import Category

from . import BLACK, BLUE, WHITE, BoardConfig

TICTACTOE = BoardConfig(
    category=Category.HORIZONTAL_BOARD,
    title="Tic Tac Toe",
    row_num=3,
    col_num=3,
    screen_width=300,
    screen_height=300,
    corner_markers=[],
    bg_grid=BLUE,
    first_player_color=BLACK,
    second_player_color=WHITE,
)
