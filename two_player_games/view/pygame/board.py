from __future__ import annotations

import sys

from two_player_games.common import (
    MARK_FIRST,
    MARK_SECOND,
    CellMark,
    Event,
    Status,
    Turn,
)
from two_player_games.config.board import BoardConfig
from two_player_games.model.board import BoardChange, BoardState
from two_player_games.model.board.horizontal import (
    HorizontalBoard,
    HorizontalBoardAction,
)
from two_player_games.view import View

try:
    import pygame
except ImportError:
    print(
        "Pygame not installed. Please install pygame to run this program.",
        file=sys.stderr,
    )
    sys.exit()


class InvalidCellMark(Exception):
    def __init__(self, mark: CellMark | int) -> None:
        super().__init__()
        self.mark = mark

    def __str__(self) -> str:
        return f"Inavlid cell mark: {self.mark}"


class PyGameBoardView(View[HorizontalBoardAction, BoardState, BoardChange]):
    def __init__(self, config: BoardConfig) -> None:
        super().__init__(**config.__dict__)
        pygame.init()
        # TODO Set an icon
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height + self.text_hight),
        )
        self.cell_width = self.screen_width // self.col_num
        self.cell_height = self.screen_height // self.row_num
        self.hints: list[pygame.Rect] = []
        self.restart()

    def get_event(self) -> Event:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Event.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key in {pygame.K_ESCAPE, pygame.K_q}:
                    return Event.QUIT
                if event.key == pygame.K_r:
                    return Event.RESTART
            if event.type == pygame.MOUSEBUTTONDOWN:
                # FIXME Check if this interferes with non-human agents
                pos_x, pos_y = pygame.mouse.get_pos()
                column = pos_x // self.cell_width
                row = pos_y // self.cell_height
                self.human_action = (row, column)
                return Event.CLICKED
        return Event.NONE

    def _render_first_player(
        self,
        pos_x: int,
        pos_y: int,
        radius: int,
    ) -> None:
        # TODO Accept functions to render pieces for different games. For
        # example, X and O for Tic-Tac-Toe.
        pygame.draw.circle(
            self.screen,
            self.first_player_color,
            (pos_x, pos_y),
            radius,
        )

    def _render_second_player(
        self,
        pos_x: int,
        pos_y: int,
        radius: int,
    ) -> None:
        # TODO Accept functions to render pieces for different games. For
        # example, X and O for Tic-Tac-Toe.
        pygame.draw.circle(
            self.screen,
            self.second_player_color,
            (pos_x, pos_y),
            radius,
        )

    def _init_scores(
        self,
    ) -> None:
        half_text_hight = self.text_hight // 2
        half_cell_width = self.cell_width // 2

        self.screen.fill(
            self.bg_scores_pane,
            (0, self.screen_height, self.screen_width, self.text_hight),
        )
        # TODO Allow custom markers for players. For example, X and O for
        # Tic-Tac-Toe.
        self._render_first_player(
            half_cell_width,
            self.screen_height + half_text_hight,
            half_text_hight - self.padding,
        )
        self._render_second_player(
            self.screen_width - half_cell_width,
            self.screen_height + half_text_hight,
            half_text_hight - self.padding,
        )

    def update_scores(
        self,
        model: HorizontalBoard,
    ) -> None:
        scores = model.scores
        current_turn = model.turn
        status = model.status

        half_screen_width = self.screen_width // 2
        half_text_hight = self.text_hight // 2
        half_cell_width = self.cell_width // 2

        first_score_surface = pygame.font.SysFont(
            self.font_family,
            self.font_size,
        ).render(
            # HACK The surrounding spaces are intentional to avoid an update
            # smaller than the previous value.
            f" {scores[Turn.FIRST]} ",
            True,
            self.first_player_color,
            self.bg_scores_pane,
        )
        self.screen.blit(
            first_score_surface,
            (
                (
                    half_screen_width
                    + half_cell_width
                    - first_score_surface.get_width()
                )
                // 2,
                self.screen_height + self.padding,
            ),
        )
        second_score_surface = pygame.font.SysFont(
            self.font_family,
            self.font_size,
        ).render(
            # HACK The surrounding spaces are intentional to avoid an update
            # smaller than the previous value.
            f" {scores[Turn.SECOND]} ",
            True,
            self.second_player_color,
            self.bg_scores_pane,
        )
        self.screen.blit(
            second_score_surface,
            (
                (
                    3 * half_screen_width
                    - half_cell_width
                    - second_score_surface.get_width()
                )
                // 2,
                self.screen_height + self.padding,
            ),
        )

        pygame.draw.circle(
            self.screen,
            (
                self.first_player_color
                if current_turn == Turn.FIRST
                else self.second_player_color
            ),
            (half_screen_width, self.screen_height + half_text_hight),
            half_text_hight - self.padding,
        )

        match status:
            case Status.FIRST_WON:
                self._render_first_player(
                    half_screen_width,
                    self.screen_height + half_text_hight,
                    half_text_hight - self.padding,
                )

                self._mark_game_over(half_screen_width, half_text_hight)
            case Status.SECOND_WON:
                self._render_second_player(
                    half_screen_width,
                    self.screen_height + half_text_hight,
                    half_text_hight - self.padding,
                )
                self._mark_game_over(half_screen_width, half_text_hight)
            case Status.DRAW:
                pygame.draw.circle(
                    self.screen,
                    self.bg_draw,
                    (half_screen_width, self.screen_height + half_text_hight),
                    half_text_hight - self.padding,
                )
                # self._mark_game_over(half_screen_width, half_text_hight)
            case _:
                pass

    def _mark_game_over(
        self,
        half_screen_width: int,
        half_text_hight: int,
    ) -> None:
        pygame.draw.circle(
            self.screen,
            self.game_over_color,
            (half_screen_width, self.screen_height + half_text_hight),
            half_text_hight - self.padding,
            self.padding,
        )

    def update_state(
        self,
        model: HorizontalBoard,
    ) -> None:
        state = model.state
        changes = model.changes
        turn = model.turn
        possible_actions = model.possible_actions

        radius = min(self.cell_width, self.cell_height) // 2 - self.padding

        self._clean_hints()

        for row, column in changes:
            pos_x = (2 * column + 1) * self.cell_width // 2 + 1
            pos_y = (2 * row + 1) * self.cell_height // 2 + 1
            mark = state[(row, column)]
            if mark == MARK_FIRST:
                self._render_first_player(pos_x, pos_y, radius)
            elif mark == MARK_SECOND:
                self._render_second_player(pos_x, pos_y, radius)
            else:
                raise InvalidCellMark(mark)
        if self.display_hint:
            self._display_hint(turn, possible_actions)

    def _display_hint(
        self,
        turn: Turn,
        possible_actions: list[HorizontalBoardAction],
    ) -> None:
        radius = min(self.cell_width, self.cell_height) // 2 - self.padding

        try:
            for row, column in possible_actions:
                pos_x = (2 * column + 1) * self.cell_width // 2 + 1
                pos_y = (2 * row + 1) * self.cell_height // 2 + 1
                self.hints.append(
                    pygame.draw.circle(
                        self.screen,
                        self.bg_draw,
                        (pos_x, pos_y),
                        radius,
                    ),
                )

                for i in range(self.hint_num):
                    ratio = (i + 1) / self.hint_num
                    self.hints.append(
                        pygame.draw.circle(
                            self.screen,
                            (
                                self.first_player_color
                                if turn == Turn.FIRST
                                else self.second_player_color
                            ),
                            (pos_x, pos_y),
                            ratio * radius,
                            self.line_thickness,
                        ),
                    )
        # HACK This works as the implemented actions are only tuple[int, int]
        # and int. We may need a more general solution if we have other action
        # types.
        except TypeError as type_error_exception:
            if type_error_exception.args == (
                "cannot unpack non-iterable int object",
            ):
                pass
            else:
                raise type_error_exception

    def _clean_hints(self) -> None:
        for hint in self.hints:
            pygame.draw.circle(
                self.screen,
                self.bg_grid,
                hint.center,
                hint.width // 2,
            )
        self.hints = []

    def refresh(self) -> None:
        pygame.display.flip()

    def restart(self) -> None:
        self.human_action = None
        self._init_grid()
        self._init_scores()
        pygame.display.flip()

    def _init_grid(self) -> None:
        self.screen.fill(self.bg_grid)
        for row in range(self.row_num + 1):
            pygame.draw.line(
                self.screen,
                self.fg_line,
                (0, row * self.cell_height),
                (self.screen_width, row * self.cell_height),
                self.line_thickness,
            )
        for column in range(self.col_num + 1):
            pygame.draw.line(
                self.screen,
                self.fg_line,
                (column * self.cell_width, 0),
                (column * self.cell_width, self.screen_height),
                self.line_thickness,
            )
        for row, column in self.corner_markers:
            pygame.draw.circle(
                self.screen,
                self.fg_line,
                (column * self.cell_width + 1, row * self.cell_height + 1),
                self.padding,
            )

    def quit(self) -> None:
        pygame.quit()
        sys.exit()

    # TODO Implement the display_menu_screen method
    def display_menu_screen(self) -> None:
        pass
        # menu_screen = pygame.Surface(
        #     (self.screen_width, self.screen_height + self.text_hight)
        # )
        # # menu_screen = self.screen.subsurface((0, 0, 100, 100))
        # menu_screen.fill(BLACK)
        # self.screen.blit(menu_screen, (0,0))
        # pygame.display.flip()

    # TODO Implement the display_help_screen method
    def display_help_screen(self) -> None:
        pass
