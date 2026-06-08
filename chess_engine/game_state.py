from chess_engine.board import Board
from chess_engine.pieces import Piece
from chess_engine.pieces import Piece
from chess_engine.board import Board
import pygame as pg

class GameState:
    def __init__(self):
        self.white_to_move = True
        self.board = Board()
        self.move_log = []
        self.PIECE_IMAGES = {}

    def load_piece_images(self):
        for piece in Piece.PIECES:
            self.PIECE_IMAGES[piece] = pg.transform.scale(
                pg.image.load(f'assets/images/chess_pieces/{piece}.png'), 
                (self.board.SQUARE_SIZE, self.board.SQUARE_SIZE)
            )

    def draw_game_state(self, screen):
        def draw_board(screen):
            colors = [pg.Color('white'), pg.Color('gray')]
            for row in range(Board().DIMENSION):
                for col in range(Board().DIMENSION):
                    pg.draw.rect(
                        screen, 
                        colors[(row + col) % 2], 
                        pg.Rect(
                            col * Board().SQUARE_SIZE, 
                            row * Board().SQUARE_SIZE, 
                            Board().SQUARE_SIZE, 
                            Board().SQUARE_SIZE
                        )
                    )

        def draw_pieces(screen, board):
            for row in range(Board().DIMENSION):
                for col in range(Board().DIMENSION):
                    piece = board[row][col]
                    if piece != '--':
                        screen.blit(
                            self.PIECE_IMAGES[piece], 
                            pg.Rect(
                                col * Board().SQUARE_SIZE, 
                                row * Board().SQUARE_SIZE, 
                                Board().SQUARE_SIZE, 
                                Board().SQUARE_SIZE 
                            )
                        )

        draw_board(screen)
        draw_pieces(screen, self.board.board)

