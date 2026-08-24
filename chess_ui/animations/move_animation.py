import pygame as pg

from chess_ui.config import MOVE_ANIMATION_DURATION_MS, SQUARE_SIZE


class MoveAnimation:
    """
    Animate one or more pieces without changing engine state.
    """

    def __init__(self):
        """
        Create an empty animation queue.
        """
        self.animations = []

    @property
    def is_animating(self):
        """
        Return `True` while at least one piece is still moving.
        """
        return bool(self.animations)

    ####################################################################################
    # ----------------------------- ANIMATION LIFECYCLE --------------------------------
    ####################################################################################

    def start(self, piece, start_square, end_square):
        """
        Queue a piece animation and return the created animation record.
        """
        animation = {
            'piece': piece,
            'start_square': start_square,
            'end_square': end_square,
            'start_time': pg.time.get_ticks(),
        }
        self.animations.append(animation)
        return animation

    def stop(self):
        """
        Discard all active animations.
        """
        self.animations.clear()

    ####################################################################################
    # ---------------------------------- RENDERING -------------------------------------
    ####################################################################################

    def draw(self, screen, piece_images):
        """
        Draw active animations and remove completed ones.
        """
        current_time = pg.time.get_ticks()
        active_animations = []

        for animation in self.animations:
            elapsed = current_time - animation['start_time']
            progress = min(elapsed / MOVE_ANIMATION_DURATION_MS, 1)

            if progress >= 1:
                continue

            position = self._interpolate_position(animation, progress)
            piece_image = piece_images.get(animation['piece'])

            if piece_image is not None:
                screen.blit(piece_image, position)

            active_animations.append(animation)

        self.animations = active_animations

    def should_skip_piece(self, square):
        """
        Return whether a board piece is currently drawn by the animator.
        """
        return any(
            animation['end_square'] == square
            for animation in self.animations
        )

    def _interpolate_position(self, animation, progress):
        """
        Return the pixel position between an animation's start and end.
        """
        start_row, start_col = animation['start_square']
        end_row, end_col = animation['end_square']

        start_x = start_col * SQUARE_SIZE
        start_y = start_row * SQUARE_SIZE
        end_x = end_col * SQUARE_SIZE
        end_y = end_row * SQUARE_SIZE

        return (
            start_x + (end_x - start_x) * progress,
            start_y + (end_y - start_y) * progress,
        )
