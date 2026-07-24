import pygame as pg
from chess_engine.helpers import EMP


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

    def get_piece(self, square):
        row, col = square
        return self.board[row][col]

    def set_piece(self, square, piece):
        row, col = square
        self.board[row][col] = piece

    def draw(self, screen, piece_images, should_skip_piece=None):
        self.draw_board(screen)
        self.draw_pieces(screen, piece_images, should_skip_piece)

    def draw_board(self, screen):
        colors = [pg.Color('white'), pg.Color('gray')]
        for row in range(self.DIMENSION):
            for col in range(self.DIMENSION):
                pg.draw.rect(
                    screen,
                    colors[(row + col) % 2],
                    self._square_rect(row, col)
                )

    def draw_pieces(self, screen, piece_images, should_skip_piece=None):
        for row in range(self.DIMENSION):
            for col in range(self.DIMENSION):
                square = (row, col)
                piece = self.board[row][col]

                if should_skip_piece is not None and should_skip_piece(square):
                    continue

                if piece != EMP:
                    screen.blit(piece_images[piece], self._square_rect(row, col))

    def _square_rect(self, row, col):
        return pg.Rect(
            col * self.SQUARE_SIZE,
            row * self.SQUARE_SIZE,
            self.SQUARE_SIZE,
            self.SQUARE_SIZE
        )