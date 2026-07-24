import pygame as pg
from chess_engine.chess_properties import Piece
from chess_engine.game_state.highlight_renderer import HighlightRenderer


class GameRenderer:
    def __init__(self, game_state):
        self.game_state = game_state
        self.highlight_renderer = HighlightRenderer(game_state)

    @property
    def board(self):
        return self.game_state.board

    def load_piece_images(self):
        for piece in Piece.PIECES:
            self.game_state.PIECE_IMAGES[piece] = pg.transform.scale(
                pg.image.load(f'assets/images/chess_pieces/{piece}.png'),
                (self.board.SQUARE_SIZE, self.board.SQUARE_SIZE)
            )

    def draw_game_state(self, screen):
        self.board.draw(screen, self.game_state.PIECE_IMAGES)
        self.highlight_renderer.draw(screen)
        self.board.draw_pieces(screen, self.game_state.PIECE_IMAGES)

        if self.game_state.promotion_pending:
            self.game_state.input_handler.promotion_ui.draw(screen)