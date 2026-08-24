from chess_engine.chess_properties import Board
from chess_engine.move import Move
from chess_engine.move.move_validator import MoveValidator
from chess_engine.game_state.game_renderer import GameRenderer
from chess_engine.game_state.input_handler import InputHandler
from chess_engine.game_state.move_animation import MoveAnimation
from chess_engine.game_state.game_over_ui import GameOverUI
import pygame as pg


class GameState:
    GAME_OVER_DELAY = 3000

    def __init__(self):
        self.white_to_move = True
        self.board = Board()
        self.move = Move(self)
        self.move_validator = MoveValidator(self)
        self.renderer = GameRenderer(self)
        self.input_handler = InputHandler(self)
        self.move_animation = MoveAnimation(self)
        self.gamemode = 'Gamemode 1'
        self.game_over_ui = GameOverUI(self)

        self.PIECE_IMAGES = {}

        self.selected_square = ()
        self.player_clicked = []

        self.moved_square = None
        self.moved_piece = None
        self.target_square = None
        self.target_piece = None

        self.black_king_position = (0, 4)
        self.white_king_position = (7, 4)

        self.promotion_pending = False
        self.promotion_square = None
        self.promotion_moved_square = None
        self.promotion_moved_piece = None
        self.promotion_target_piece = None
        self.promotion_color = None

        self.en_passant_target = None
        self.last_double_pawn_move = None

        self.castling_rights = {
            'w': {'king_side': True, 'queen_side': True},
            'b': {'king_side': True, 'queen_side': True}
        }
        self.castling_rights_log = []

        self.hovered_square = None
        self.selected_legal_moves = []

        self.game_over = False
        self.game_result = None       # 'checkmate' or 'stalemate'
        self.winner = None            # 'WHITE WINS', 'BLACK WINS', or None
        self.game_over_started_at = None

    def load_piece_images(self):
        self.renderer.load_piece_images()

    def draw_game_state(self, screen):
        self.renderer.draw_game_state(screen)

    def handle_mouse_click(self, mouse_location):
        if self.game_over:
            return self.game_over_ui.handle_click(mouse_location)

        self.input_handler.handle_mouse_click(mouse_location)
        return None
    
    def handle_mouse_motion(self, mouse_location):
        self.input_handler.handle_mouse_motion(mouse_location)

    def finish_turn(self):
        """
        Switches turns and evaluates the new side-to-move.

        Returns:
            A (move_status, match_result) tuple. move_status is CHECK,
            CHECKMATE, STALEMATE, or None. match_result is only set when
            the match ends.
        """
        self.white_to_move = not self.white_to_move

        if self.move_validator.is_checkmate():
            winner = 'BLACK WINS!' if self.white_to_move else 'WHITE WINS!'
            self._set_game_over(
                result='checkmate',
                winner=winner
            )
            return 'CHECKMATE', winner

        if self.move_validator.is_stalemate():
            self._set_game_over(
                result='stalemate',
                winner=None
            )
            return 'STALEMATE', 'DRAW!'

        if self.move_validator.in_check():
            return 'CHECK', None

        return None, None

    def _set_game_over(self, result, winner):
        self.game_over = True
        self.game_result = result
        self.winner = winner
        self.game_over_started_at = pg.time.get_ticks()

        self.selected_square = ()
        self.player_clicked = []
        self.selected_legal_moves = []

    def get_game_over_elapsed(self):
        if self.game_over_started_at is None:
            return 0

        return pg.time.get_ticks() - self.game_over_started_at

    def get_losing_king_square(self):
        return (
            self.white_king_position
            if self.white_to_move
            else self.black_king_position
        )
