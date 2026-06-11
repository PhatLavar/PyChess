from chess_engine.chess_properties import Board, Animation
from chess_engine.game_state import GameState
from chess_engine.move import Move
import pygame as pg

def chess():
    pg.init()
    
    screen = pg.display.set_mode((Board.SCREEN_SIZE, Board.SCREEN_SIZE))
    clock = pg.time.Clock()
    screen.fill('white')

    game_state = GameState()
    game_state.load_piece_images()
    
    game_loop(game_state, clock, screen, game_state.move)


def game_loop(game_state, clock, screen, move):
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                game_state.handle_mouse_click(pg.mouse.get_pos())
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    game_state.move.handle_undo_move()
        
        game_state.draw_game_state(screen)
        pg.display.update()
        clock.tick(Animation().MAX_FPS) #60 FPS


if __name__ == '__main__':
    chess()