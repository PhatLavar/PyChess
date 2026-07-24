import pygame as pg
from chess_engine.helpers import EMP, piece_color, turn_color

class HighlightRenderer:
    def __init__(self, game_state):
        self.game_state = game_state

    @property
    def board(self):
        return self.game_state.board

    def draw(self, screen):
        self._draw_hover_highlight(screen)
        self._draw_selected_square_highlight(screen)
        self._draw_legal_move_highlights(screen)
        self._draw_checked_king_highlight(screen)

    def _draw_hover_highlight(self, screen):
        square = self.game_state.hovered_square

        if square is None:
            return

        self._draw_square_overlay(
            screen,
            square,
            color=(153, 255, 102),
            alpha=70
        )

    def _draw_selected_square_highlight(self, screen):
        square = self.game_state.selected_square

        if square == ():
            return

        self._draw_square_overlay(
            screen,
            square,
            color=(0, 180, 255),
            alpha=130
        )

    def _draw_legal_move_highlights(self, screen):
        for target_square in self.game_state.selected_legal_moves:
            target_piece = self.board.get_piece(target_square)

            if target_piece == EMP:
                self._draw_square_overlay(
                    screen,
                    target_square,
                    color=(0, 200, 255),
                    alpha=110
                )
            else:
                self._draw_square_overlay(
                    screen,
                    target_square,
                    color=(255, 40, 40),
                    alpha=130
                )

    def _draw_checked_king_highlight(self, screen):
        validator = self.game_state.move_validator

        if validator.in_check('w'):
            self._draw_square_overlay(
                screen,
                self.game_state.white_king_position,
                color=(255, 0, 0),
                alpha=150
            )

        if validator.in_check('b'):
            self._draw_square_overlay(
                screen,
                self.game_state.black_king_position,
                color=(255, 0, 0),
                alpha=150
            )

    def _draw_square_overlay(self, screen, square, color, alpha):
        row, col = square

        overlay = pg.Surface(
            (self.board.SQUARE_SIZE, self.board.SQUARE_SIZE),
            pg.SRCALPHA
        )

        overlay.fill((*color, alpha))

        screen.blit(
            overlay,
            (
                col * self.board.SQUARE_SIZE,
                row * self.board.SQUARE_SIZE
            )
        )