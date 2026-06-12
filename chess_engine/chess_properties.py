import pygame as pg
from chess_engine.helper import EMP
MAX_FPS = 60


####################################################################################
# ------------------------------------ PIECES --------------------------------------
####################################################################################
class Piece:
    PIECES = [
        'bR', 'bN', 'bB', 'bQ', 'bK', 'bP', 
        'wR', 'wN', 'wB', 'wQ', 'wK', 'wP',
    ]

    def __init__(self):
        pass


####################################################################################
# ------------------------------------- BOARD --------------------------------------
####################################################################################
class Board:
    SCREEN_SIZE = 512
    DIMENSION = 8
    SQUARE_SIZE = SCREEN_SIZE // DIMENSION
    
    def __init__(self):
        self.WIDTH = self.HEIGHT = Board.SCREEN_SIZE
        self.DIMENSION = Board.DIMENSION
        self.SQUARE_SIZE = Board.SQUARE_SIZE

        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
            [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
            [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
            [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]

    ####################################################################################
    # ----------------------------- PIECE GETTER & SETTER ------------------------------
    ####################################################################################
    def get_piece(self, square):
        row, col = square
        return self.board[row][col]

    def set_piece(self, square, piece):
        row, col = square
        self.board[row][col] = piece


    ####################################################################################
    # ------------------------------- DRAW GAME SCREEN ---------------------------------
    ####################################################################################
    def draw(self, screen, piece_images):
        self.draw_board(screen)
        self.draw_pieces(screen, piece_images)

    def draw_board(self, screen):
        colors = [pg.Color('white'), pg.Color('gray')]
        for row in range(self.DIMENSION):
            for col in range(self.DIMENSION):
                pg.draw.rect(
                    screen,
                    colors[(row + col) % 2],
                    self._square_rect(row, col)
                )

    def draw_pieces(self, screen, piece_images):
        for row in range(self.DIMENSION):
            for col in range(self.DIMENSION):
                piece = self.board[row][col]
                if piece != EMP:
                    screen.blit(piece_images[piece], self._square_rect(row, col))

    def _square_rect(self, row, col):
        return pg.Rect(
            col * self.SQUARE_SIZE,
            row * self.SQUARE_SIZE,
            self.SQUARE_SIZE,
            self.SQUARE_SIZE
        )
