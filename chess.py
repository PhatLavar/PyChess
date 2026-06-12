from chess_engine.chess_properties import Board, MAX_FPS
from chess_engine.game_state import GameState
import pygame as pg


class ChessGame:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((Board.SCREEN_SIZE, Board.SCREEN_SIZE))
        self.clock = pg.time.Clock()
        self.game_state = GameState()
        self.game_state.load_piece_images()


    ####################################################################################
    # -------------------------------- RUN CHESS GAME ----------------------------------
    ####################################################################################
    def run(self):
        running = True
        while running:
            running = self._handle_events()
            self._draw()
            self.clock.tick(MAX_FPS)


    ####################################################################################
    # ------------------------ DRAW GAME STATE + HANDLE EVENT --------------------------
    ####################################################################################
    def _handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.game_state.handle_mouse_click(pg.mouse.get_pos())
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    self.game_state.move.handle_undo_move()
        return True

    def _draw(self):
        self.game_state.draw_game_state(self.screen)
        pg.display.update()


if __name__ == '__main__':
    ChessGame().run()
