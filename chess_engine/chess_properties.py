import pygame as pg

class Piece:
    PIECES = [
        'bR', 'bN', 'bB', 'bQ', 'bK', 'bP', 
        'wR', 'wN', 'wB', 'wQ', 'wK', 'wP',
    ]

    def __init__(self):
        pass

    def draw_pieces(self, screen, pieces):
        pass



class Board:
    SCREEN_SIZE = 512
    DIMENSION = 8
    SQUARE_SIZE = SCREEN_SIZE // DIMENSION
    
    def __init__(self):
        self.WIDTH = self.HEIGHT = Board.SCREEN_SIZE
        self.DIMENSION = Board.DIMENSION
        self.SQUARE_SIZE = Board.SQUARE_SIZE

        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bN', 'bB', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wN', 'wB', 'wR'],
        ]



class Animation:
    def __init__(self):
        self.MAX_FPS = 60