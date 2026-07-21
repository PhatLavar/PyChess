import pygame as pg
from chess_engine.chess_properties import Board


class PromotionUI:
    def __init__(self, game_state):
        self.game_state = game_state

    def draw(self, screen):
        overlay = pg.Surface((Board.SCREEN_SIZE, Board.SCREEN_SIZE))
        overlay.set_alpha(180)
        overlay.fill(pg.Color('lightgray'))
        screen.blit(overlay, (0, 0))

        for piece_type, rect in self.choice_rects():
            piece = self.game_state.promotion_color + piece_type
            pg.draw.rect(screen, pg.Color('white'), rect)
            pg.draw.rect(screen, pg.Color('black'), rect, 2)

            if piece in self.game_state.PIECE_IMAGES:
                screen.blit(self.game_state.PIECE_IMAGES[piece], rect)

    def handle_click(self, mouse_location):
        for chosen_type, rect in self.choice_rects():
            if rect.collidepoint(mouse_location):
                self.game_state.move.executor.handle_pawn_promotion(chosen_type)
                return

    def choice_rects(self):
        pieces = ['Q', 'R', 'B', 'N']
        gap = Board.SQUARE_SIZE // 3
        total_width = len(pieces) * Board.SQUARE_SIZE + (len(pieces) - 1) * gap
        start_x = Board.SCREEN_SIZE // 2 - total_width // 2
        y = Board.SCREEN_SIZE // 2 - Board.SQUARE_SIZE // 2

        return [
            (
                piece_type,
                pg.Rect(
                    start_x + index * (Board.SQUARE_SIZE + gap),
                    y,
                    Board.SQUARE_SIZE,
                    Board.SQUARE_SIZE
                )
            )
            for index, piece_type in enumerate(pieces)
        ]