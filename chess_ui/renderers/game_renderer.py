from pathlib import Path

import pygame as pg

from chess_engine.core import Piece
from chess_engine.utilities import EMP
from chess_ui.config import (
    BOARD_DARK_COLOR,
    BOARD_DIMENSION,
    BOARD_LIGHT_COLOR,
    PIECE_IMAGE_DIRECTORY,
    SQUARE_SIZE,
)
from chess_ui.renderers.highlight_renderer import HighlightRenderer


class GameRenderer:
    """Render the board, pieces, interactions, animations, and modal screens."""

    def __init__(
        self,
        game_state,
        input_handler,
        move_animation,
        game_over_ui,
    ):
        """Bind the renderer to one match and its presentation components."""
        self.game_state = game_state
        self.input_handler = input_handler
        self.move_animation = move_animation
        self.game_over_ui = game_over_ui
        self.highlight_renderer = HighlightRenderer(game_state, input_handler)
        self.piece_images = {}

    # Assets

    def load_piece_images(self):
        """Load and scale every piece image; return the resulting image map."""
        image_directory = Path(PIECE_IMAGE_DIRECTORY)

        for piece in Piece.PIECES:
            image_path = image_directory / f'{piece}.png'
            self.piece_images[piece] = pg.transform.scale(
                pg.image.load(str(image_path)),
                (SQUARE_SIZE, SQUARE_SIZE),
            )

        return self.piece_images

    # Frame rendering

    def draw(self, screen):
        """Draw one complete application frame in layer order."""
        self._draw_board(screen)
        self.highlight_renderer.draw(screen)
        self._draw_pieces(screen)
        self.move_animation.draw(screen, self.piece_images)

        if self.game_state.promotion_pending:
            self.input_handler.promotion_ui.draw(screen, self.piece_images)

        self.game_over_ui.draw(screen)

    def _draw_board(self, screen):
        """Draw the alternating board squares."""
        colors = (pg.Color(BOARD_LIGHT_COLOR), pg.Color(BOARD_DARK_COLOR))

        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                square_rect = pg.Rect(
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                )
                pg.draw.rect(screen, colors[(row + col) % 2], square_rect)

    def _draw_pieces(self, screen):
        """Draw stationary pieces, skipping those owned by the animator."""
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                square = row, col
                piece = self.game_state.board.get_piece(square)

                if piece == EMP or self.move_animation.should_skip_piece(square):
                    continue

                screen.blit(
                    self.piece_images[piece],
                    (col * SQUARE_SIZE, row * SQUARE_SIZE),
                )
