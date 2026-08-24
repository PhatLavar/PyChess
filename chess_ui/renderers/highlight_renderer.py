import pygame as pg

from chess_engine.utilities import EMP
from chess_ui.config import (
    CAPTURE_ALPHA,
    CAPTURE_COLOR,
    CHECK_ALPHA,
    CHECK_COLOR,
    HOVER_ALPHA,
    HOVER_COLOR,
    LEGAL_MOVE_ALPHA,
    LEGAL_MOVE_COLOR,
    SELECTED_ALPHA,
    SELECTED_COLOR,
    SQUARE_SIZE,
)


class HighlightRenderer:
    """Draw board interaction and king-safety highlights."""

    def __init__(self, game_state, input_handler):
        """Bind engine state and application selection state."""
        self.game_state = game_state
        self.input_handler = input_handler

    @property
    def board(self):
        """Return the active engine board."""
        return self.game_state.board

    # Rendering

    def draw(self, screen):
        """Draw all applicable highlights in visual-priority order."""
        self._draw_hover_highlight(screen)
        self._draw_selected_square_highlight(screen)
        self._draw_legal_move_highlights(screen)
        self._draw_checked_king_highlight(screen)

    def _draw_hover_highlight(self, screen):
        """Draw the current board hover, when one exists."""
        square = self.input_handler.hovered_square

        if square is not None:
            self._draw_square_overlay(screen, square, HOVER_COLOR, HOVER_ALPHA)

    def _draw_selected_square_highlight(self, screen):
        """Draw the currently selected origin square."""
        square = self.input_handler.selected_square

        if square != self.input_handler.NO_SQUARE:
            self._draw_square_overlay(
                screen,
                square,
                SELECTED_COLOR,
                SELECTED_ALPHA,
            )

    def _draw_legal_move_highlights(self, screen):
        """Draw legal targets, distinguishing quiet moves from captures."""
        for target_square in self.input_handler.selected_legal_moves:
            is_capture = self.board.get_piece(target_square) != EMP
            color = CAPTURE_COLOR if is_capture else LEGAL_MOVE_COLOR
            alpha = CAPTURE_ALPHA if is_capture else LEGAL_MOVE_ALPHA
            self._draw_square_overlay(screen, target_square, color, alpha)

    def _draw_checked_king_highlight(self, screen):
        """Draw checked kings unless the terminal animation owns the square."""
        if self.game_state.game_over:
            return

        validator = self.game_state.move_validator

        if validator.in_check('w'):
            self._draw_square_overlay(
                screen,
                self.game_state.white_king_position,
                CHECK_COLOR,
                CHECK_ALPHA,
            )

        if validator.in_check('b'):
            self._draw_square_overlay(
                screen,
                self.game_state.black_king_position,
                CHECK_COLOR,
                CHECK_ALPHA,
            )

    def _draw_square_overlay(self, screen, square, color, alpha):
        """Draw a translucent color overlay on one board square."""
        row, col = square
        overlay = pg.Surface((SQUARE_SIZE, SQUARE_SIZE), pg.SRCALPHA)
        overlay.fill((*color, alpha))
        screen.blit(overlay, (col * SQUARE_SIZE, row * SQUARE_SIZE))
