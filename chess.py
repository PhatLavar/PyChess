from chess_engine.board import Board
from chess_engine.game_state import GameState
from chess_engine.animation import Animation
import pygame as pg

def chess():
    pg.init()
    
    screen = pg.display.set_mode((Board.SCREEN_SIZE, Board.SCREEN_SIZE))
    clock = pg.time.Clock()
    screen.fill('white')

    game_state = GameState()
    game_state.load_piece_images()
    
    ############################################# 
    # GAME LOOP
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        game_state.draw_game_state(screen)
        pg.display.update()
        clock.tick(Animation().MAX_FPS)
    # Stardard = 15 FPS
    #############################################

if __name__ == '__main__':
    chess()