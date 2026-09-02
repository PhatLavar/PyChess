import pygame as pg

from chess_app.config import (
    BOT_MOVE_DELAY_MS,
    MATCH_HISTORY_SEPARATOR_CHARACTER,
    MATCH_HISTORY_SEPARATOR_LENGTH,
    MATCH_HISTORY_SEPARATOR_LINES,
    MAX_FPS,
)
from chess_app.event_handler import EventHandler
from chess_app.input_handler import InputHandler
from chess_app.match_history import MatchHistory
from chess_engine import GameState
from chess_engine.bots import EasyBot, HardBot, ImpossibleBot, MasterBot, MediumBot
from chess_engine.moves.execution.move_executor import MoveExecutor
from chess_ui.animations import MoveAnimation
from chess_ui.config import BOARD_PIXEL_SIZE
from chess_ui.renderers import GameRenderer
from chess_ui.screens import GameOverUI, StartMenuUI


class ChessGame:
    """
    Coordinate the Pygame lifecycle, chess engine, and user interface.
    """

    PLAYER_MODE = 'player'
    BOT_MODE = 'bot'
    BOT_BOT_MODE = 'bot_bot'
    START_SCREEN = 'start'
    GAME_SCREEN = 'game'
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

        self.active_screen = self.START_SCREEN
        self.gamemode = None
        self.bot_difficulty = None
        self.bot = None
        self.white_bot = None
        self.bot_wait_started_at = None

        self.start_menu_ui = StartMenuUI()
        self.event_handler = EventHandler(self)
        self.match_history = MatchHistory()
        self.match_history.ensure_directory()

        self.game_state = None
        self.input_handler = None
        self.game_over_ui = None
        self.renderer = None
        self.move_animation = None
        self.match_history_saved = False

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
    
    def start_player_game(self):
        """
        Start the existing local player-versus-player game.
        """
        self.gamemode = self.PLAYER_MODE
        self.bot_difficulty = None
        self.bot = None
        self.white_bot = None
        self.bot_wait_started_at = None
        self.active_screen = self.GAME_SCREEN
        self._create_match()

    def start_bot_game(self, difficulty):
        """
        Start a bot-mode match with the player as White.
        """
        self.gamemode = self.BOT_MODE
        self.bot_difficulty = difficulty
        bot_type = self._get_bot_type(difficulty)
        self.bot = bot_type() if bot_type is not None else None
        self.white_bot = None
        self.bot_wait_started_at = None
        self.active_screen = self.GAME_SCREEN
        self._create_match()

    def start_bot_bot_game(self, difficulty):
        """Start a spectator match with equally skilled bots on both sides."""
        self.gamemode = self.BOT_BOT_MODE
        self.bot_difficulty = difficulty
        bot_type = self._get_bot_type(difficulty)
        self.white_bot = bot_type() if bot_type is not None else None
        self.bot = bot_type() if bot_type is not None else None
        self.bot_wait_started_at = None
        self.active_screen = self.GAME_SCREEN
        self._create_match()

    @staticmethod
    def _get_bot_type(difficulty):
        """Return the bot class registered for a difficulty name."""
        bot_types = {
            'easy': EasyBot,
            'medium': MediumBot,
            'hard': HardBot,
            'master': MasterBot,
            'impossible': ImpossibleBot,
        }
        return bot_types.get(difficulty)

    @property
    def active_bot(self):
        """Return the bot that owns the current turn, if any."""
        if self.game_state is None or self.game_state.game_over:
            return None
        if self.gamemode == self.BOT_BOT_MODE:
            return self.white_bot if self.game_state.white_to_move else self.bot
        if self.gamemode == self.BOT_MODE and not self.game_state.white_to_move:
            return self.bot
        return None

    @property
    def is_bot_turn(self):
        """Return whether the configured Black bot owns the current turn."""
        return self.active_bot is not None

    def _play_bot_turn(self):
        """Play and animate one Black bot move when the board is ready."""
        if not self.is_bot_turn:
            self.bot_wait_started_at = None
            return False

        if self.move_animation.is_animating:
            self.bot_wait_started_at = None
            return False

        current_time = pg.time.get_ticks()

        if self.bot_wait_started_at is None:
            self.bot_wait_started_at = current_time
            return False

        if current_time - self.bot_wait_started_at < BOT_MOVE_DELAY_MS:
            return False

        active_bot = self.active_bot
        if active_bot is None:
            return False

        move = active_bot.choose_move(self.game_state)
        if move is None:
            return False

        outcome = self.game_state.move.handle_piece_move(*move)

        if outcome == MoveExecutor.PROMOTION_PENDING:
            promotion_choice = getattr(active_bot, 'promotion_choice', 'Q')
            self.game_state.move.executor.handle_pawn_promotion(
                promotion_choice
            )
        elif outcome != MoveExecutor.MOVED:
            return False

        self.input_handler.animate_latest_move()
        self.bot_wait_started_at = None
        return True

    def handle_undo(self):
        """Undo one move in PvP or one complete player turn in bot mode."""
        if self.game_state is None:
            return False

        if self.gamemode == self.BOT_BOT_MODE:
            return False

        self.bot_wait_started_at = None

        if self.gamemode != self.BOT_MODE or self.bot is None:
            return self.input_handler.handle_undo()

        moves_to_undo = 2 if self.game_state.white_to_move else 1
        state_changed = False

        for _ in range(moves_to_undo):
            if not self.input_handler.handle_undo():
                break
            state_changed = True

        return state_changed
    
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
        self.bot_wait_started_at = None
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

    def terminate_match(self):
        """
        Record and save an unfinished match when the window is closed.

        Returns:
            The saved history `Path`, or `None` 
            when this match was already saved.
        """
        for bot in (getattr(self, 'white_bot', None), self.bot):
            if bot is not None and hasattr(bot, 'close'):
                bot.close()

        if self.game_state is None or self.match_history_saved:
            return None

        if not self.game_state.game_over:
            self.game_state.move.record_end_match('TERMINATED')

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
        if self.active_screen == self.START_SCREEN:
            self.start_menu_ui.draw(self.screen)
            pg.display.flip()
            return

        self._play_bot_turn()

        if self.game_state.game_over:
            self.game_over_ui.activate()
            self._save_completed_match()

        self.renderer.draw(self.screen)
        pg.display.flip()
