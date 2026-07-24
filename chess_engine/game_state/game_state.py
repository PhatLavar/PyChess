from chess_engine.chess_properties import Board
from chess_engine.move import Move
from chess_engine.move.move_validator import MoveValidator
from chess_engine.game_state.game_renderer import GameRenderer
from chess_engine.game_state.input_handler import InputHandler
from chess_engine.game_state.move_animation import MoveAnimation


class GameState:
    def __init__(self):
        self.white_to_move = True
        self.board = Board()
        self.move = Move(self)
        self.move_validator = MoveValidator(self)
        self.renderer = GameRenderer(self)
        self.input_handler = InputHandler(self)
        self.move_animation = MoveAnimation(self)

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

    def load_piece_images(self):
        self.renderer.load_piece_images()

    def draw_game_state(self, screen):
        self.renderer.draw_game_state(screen)

    def handle_mouse_click(self, mouse_location):
        self.input_handler.handle_mouse_click(mouse_location)
    
    def handle_mouse_motion(self, mouse_location):
        self.input_handler.handle_mouse_motion(mouse_location)