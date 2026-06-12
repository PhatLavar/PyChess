from chess_engine.chess_properties import Board, Piece
from chess_engine.helper import EMP, piece_color, turn_color
from chess_engine.move import Move
from chess_engine.move_validator import MoveValidator
import pygame as pg

class GameState:
    def __init__(self):
        self.white_to_move = True
        self.board = Board()
        self.move = Move(self)
        self.move_validator = MoveValidator(self)

        self.PIECE_IMAGES = {}
        self.selected_square = ()   # (row, col)
        self.player_clicked = []    # [(moved_row, moved_col), (target_row, target_col)]

        self.moved_square = None
        self.moved_piece = None
        self.target_square = None
        self.target_piece = None

        self.black_king_position = (0, 4)
        self.white_king_position = (7, 4)


    ####################################################################################
    # ----------------------------- DRAW BOARD AND PIECES ------------------------------
    ####################################################################################
    def load_piece_images(self):
        for piece in Piece.PIECES:
            self.PIECE_IMAGES[piece] = pg.transform.scale(
                pg.image.load(f'assets/images/chess_pieces/{piece}.png'), 
                (self.board.SQUARE_SIZE, self.board.SQUARE_SIZE)
            )

    def draw_game_state(self, screen):
        self.board.draw(screen, self.PIECE_IMAGES)


    ####################################################################################
    # --------------------------- HANDLE CLICK INTERACTION -----------------------------
    ####################################################################################
    def handle_mouse_click(self, mouse_location):
        square = self._get_square(mouse_location)
        piece = self.board.get_piece(square)

        if self._should_reset_selection(square, piece):
            self._reset_selection()
            return

        self._select_square(square)
        if len(self.player_clicked) == 2:
            self._execute_selected_move()


    ####################################################################################
    # ----------------------------- HANDLE CLICK HELPERS -------------------------------
    ####################################################################################
    def _get_square(self, mouse_location):
        col = mouse_location[0] // self.board.SQUARE_SIZE
        row = mouse_location[1] // self.board.SQUARE_SIZE
        return (row, col)

    def _should_reset_selection(self, square, piece):
        if square == self.selected_square: return True
        if len(self.player_clicked) != 0: return False
        return piece == EMP or piece_color(piece) != turn_color(self.white_to_move)

    def _reset_selection(self):
        self.selected_square = ()
        self.player_clicked = []

    def _select_square(self, square):
        self.selected_square = square
        self.player_clicked.append(square)

    def _execute_selected_move(self):
        self.moved_square = self.player_clicked[0]
        self.target_square = self.player_clicked[1]
        self.moved_piece = self.board.get_piece(self.moved_square)
        self.target_piece = self.board.get_piece(self.target_square)
        self.move.handle_piece_move(self.moved_square, self.target_square)
