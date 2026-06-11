from chess_engine.board import Board
from chess_engine.pieces import Piece
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
        def draw_board(screen):
            colors = [pg.Color('white'), pg.Color('gray')]
            for row in range(self.board.DIMENSION):
                for col in range(self.board.DIMENSION):
                    pg.draw.rect(
                        screen, 
                        colors[(row + col) % 2], 
                        pg.Rect(
                            col * self.board.SQUARE_SIZE, 
                            row * self.board.SQUARE_SIZE, 
                            self.board.SQUARE_SIZE, 
                            self.board.SQUARE_SIZE
                        )
                    )

        def draw_pieces(screen, board):
            for row in range(self.board.DIMENSION):
                for col in range(self.board.DIMENSION):
                    piece = board[row][col]
                    if piece != '--':
                        screen.blit(
                            self.PIECE_IMAGES[piece], 
                            pg.Rect(
                                col * self.board.SQUARE_SIZE, 
                                row * self.board.SQUARE_SIZE, 
                                self.board.SQUARE_SIZE, 
                                self.board.SQUARE_SIZE 
                            )
                        )

        draw_board(screen)
        draw_pieces(screen, self.board.board)



    ####################################################################################
    # --------------------------- HANDLE CLICK INTERACTION -----------------------------
    ####################################################################################
    def handle_mouse_click(self, mouse_location):
        col = mouse_location[0] // self.board.SQUARE_SIZE
        row = mouse_location[1] // self.board.SQUARE_SIZE
        piece = self.board.board[row][col]
        
        if (row, col) == self.selected_square or (self.board.board[row][col] == '--' and len(self.player_clicked) == 0):
            self.selected_square = ()
            self.player_clicked = []
        elif (self.white_to_move and piece[0] == 'b') or (not self.white_to_move and piece[0] == 'w'):
            self.selected_square = ()
            self.player_clicked = []
        else:
            self.selected_square = (row, col)
            self.player_clicked.append((row, col))
            if len(self.player_clicked) == 2:
                self.moved_square = self.player_clicked[0]
                self.target_square = self.player_clicked[1]
                self.moved_piece = self.board.board[self.moved_square[0]][self.moved_square[1]]
                self.target_piece = self.board.board[self.target_square[0]][self.target_square[1]]
                self.move.handle_piece_move(self.moved_square, self.target_square)