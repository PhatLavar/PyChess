import pygame as pg

from chess_ui.config import (
    BOARD_PIXEL_SIZE,
    BUTTON_BORDER_WIDTH,
    PROMOTION_BUTTON_GAP_RATIO,
    PROMOTION_BUTTON_BORDER_COLOR,
    PROMOTION_BUTTON_COLOR,
    PROMOTION_BUTTON_HOVER_COLOR,
    PROMOTION_OVERLAY_ALPHA,
    PROMOTION_PIECES,
    SQUARE_SIZE,
)


class PromotionUI:
    """Draw promotion choices and translate clicks into piece types."""

    def __init__(self, game_state):
        """Bind the screen to the engine state containing promotion details."""
        self.game_state = game_state

    # Rendering

    def draw(self, screen, piece_images):
        """Draw the promotion modal with light-gray hover feedback."""
        overlay = pg.Surface((BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE))
        overlay.set_alpha(PROMOTION_OVERLAY_ALPHA)
        overlay.fill(pg.Color('lightgray'))
        screen.blit(overlay, (0, 0))

        mouse_position = pg.mouse.get_pos()

        for piece_type, button_rect in self.choice_rects():
            piece = self.game_state.promotion_color + piece_type
            is_hovered = button_rect.collidepoint(mouse_position)
            button_color = pg.Color(
                PROMOTION_BUTTON_HOVER_COLOR
                if is_hovered
                else PROMOTION_BUTTON_COLOR
            )

            pg.draw.rect(screen, button_color, button_rect)
            pg.draw.rect(
                screen,
                pg.Color(PROMOTION_BUTTON_BORDER_COLOR),
                button_rect,
                width=BUTTON_BORDER_WIDTH,
            )

            if piece in piece_images:
                screen.blit(piece_images[piece], button_rect)

    # Interaction

    def get_choice(self, mouse_location):
        """Return ``Q``, ``R``, ``B``, or ``N`` when a choice is clicked.

        Returns:
            The selected promotion piece type, or ``None`` when the click is
            outside every promotion button.
        """
        for piece_type, button_rect in self.choice_rects():
            if button_rect.collidepoint(mouse_location):
                return piece_type
        return None

    def choice_rects(self):
        """Return ordered ``(piece_type, rectangle)`` promotion choices."""
        gap = int(SQUARE_SIZE * PROMOTION_BUTTON_GAP_RATIO)
        choices_width = len(PROMOTION_PIECES) * SQUARE_SIZE
        gaps_width = (len(PROMOTION_PIECES) - 1) * gap
        start_x = (BOARD_PIXEL_SIZE - choices_width - gaps_width) // 2
        start_y = (BOARD_PIXEL_SIZE - SQUARE_SIZE) // 2

        return [
            (
                piece_type,
                pg.Rect(
                    start_x + index * (SQUARE_SIZE + gap),
                    start_y,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                ),
            )
            for index, piece_type in enumerate(PROMOTION_PIECES)
        ]
