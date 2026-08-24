import pygame as pg

from chess_app.config import MAX_FPS
from chess_app.event_handler import EventHandler
from chess_app.input_handler import InputHandler
from chess_engine import GameState
from chess_ui.animations import MoveAnimation
from chess_ui.config import BOARD_PIXEL_SIZE
from chess_ui.renderers import GameRenderer
from chess_ui.screens import GameOverUI


class ChessGame:
    """Coordinate the Pygame lifecycle, chess engine, and user interface."""

    DEFAULT_GAMEMODE = 'Gamemode 1'
    WINDOW_TITLE = 'PyChess'

    def __init__(self):
        """Initialize Pygame and create the first match."""
        pg.init()
        pg.display.set_caption(self.WINDOW_TITLE)

        self.screen = pg.display.set_mode(
            (BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE)
        )
        self.clock = pg.time.Clock()
        self.gamemode = self.DEFAULT_GAMEMODE
        self.event_handler = EventHandler(self)

        self.rematch()

    # Application lifecycle

    def run(self):
        """Run frames until the user closes the window."""
        running = True

        while running:
            running = self.event_handler.process_events()
            self.draw()
            self.clock.tick(MAX_FPS)

        pg.quit()

    # Match management

    def rematch(self):
        """Replace match and presentation state while preserving gamemode."""
        self.game_state = GameState()
        self.move_animation = MoveAnimation()
        self.input_handler = InputHandler(
            self.game_state,
            self.move_animation,
        )
        self.game_over_ui = GameOverUI(
            self.game_state,
            self.gamemode,
        )
        self.renderer = GameRenderer(
            self.game_state,
            self.input_handler,
            self.move_animation,
            self.game_over_ui,
        )
        self.renderer.load_piece_images()

    def change_gamemode(self, gamemode):
        """Store a confirmed mock gamemode and return its name."""
        self.gamemode = gamemode
        return self.gamemode

    # Rendering

    def draw(self):
        """Draw and present one complete application frame."""
        self.renderer.draw(self.screen)
        pg.display.flip()
