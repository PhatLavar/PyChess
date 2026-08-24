import pygame as pg

from chess_app.config import (
    MATCH_HISTORY_SEPARATOR_CHARACTER,
    MATCH_HISTORY_SEPARATOR_LENGTH,
    MATCH_HISTORY_SEPARATOR_LINES,
    MAX_FPS,
)
from chess_app.event_handler import EventHandler
from chess_app.input_handler import InputHandler
from chess_app.match_history import MatchHistory
from chess_engine import GameState
from chess_ui.animations import MoveAnimation
from chess_ui.config import BOARD_PIXEL_SIZE
from chess_ui.renderers import GameRenderer
from chess_ui.screens import GameOverUI


class ChessGame:
    """
    Coordinate the Pygame lifecycle, chess engine, and user interface.
    """

    DEFAULT_GAMEMODE = 'Gamemode 1'
    WINDOW_TITLE = 'PyChess'

    def __init__(self):
        """
        Initialize Pygame and create the first match.
        """
        pg.init()
        pg.display.set_caption(self.WINDOW_TITLE)

        self.screen = pg.display.set_mode(
            (BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE)
        )
        self.clock = pg.time.Clock()
        self.gamemode = self.DEFAULT_GAMEMODE
        self.event_handler = EventHandler(self)
        self.match_history = MatchHistory()
        self.match_history.ensure_directory()

        self._create_match()

    ####################################################################################
    # ---------------------------- APPLICATION LIFECYCLLE ------------------------------
    ####################################################################################

    def run(self):
        """
        Run frames until the user closes the window.
        """
        running = True

        while running:
            running = self.event_handler.process_events()
            self.draw()
            self.clock.tick(MAX_FPS)

        pg.quit()

    ####################################################################################
    # ------------------------------- MATCH MANAGEMENT ---------------------------------
    ####################################################################################

    def rematch(self):
        """
        Print a terminal separator and start a fresh match.
        """
        self._print_match_separator()
        self._create_match()

    def _create_match(self):
        """
        Replace match and presentation state while preserving gamemode.
        """
        self.game_state = GameState()
        self.match_history_saved = False
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

    def _save_completed_match(self):
        """
        Save a terminal match exactly once.

        Returns:
            The saved history `Path`, or `None` while the match continues
            or after this match has already been saved.
        """
        if not self.game_state.game_over or self.match_history_saved:
            return None

        history_path = self.match_history.save(
            self.game_state.move.move_log
        )
        self.match_history_saved = True
        return history_path

    def _print_match_separator(self):
        """
        Print three separator lines without modifying either move logger.
        """
        separator = (
            MATCH_HISTORY_SEPARATOR_CHARACTER
            * MATCH_HISTORY_SEPARATOR_LENGTH
        )

        for _ in range(MATCH_HISTORY_SEPARATOR_LINES):
            print(separator)

    def change_gamemode(self, gamemode):
        """
        Store a confirmed mock gamemode and return its name.
        """
        self.gamemode = gamemode
        return self.gamemode

    ####################################################################################
    # ---------------------------------- RENDERING -------------------------------------
    ####################################################################################

    def draw(self):
        """
        Draw and present one complete application frame.
        """
        if self.game_state.game_over:
            self.game_over_ui.activate()
            self._save_completed_match()

        self.renderer.draw(self.screen)
        pg.display.flip()
