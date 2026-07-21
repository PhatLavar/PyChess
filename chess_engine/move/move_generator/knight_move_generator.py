from chess_engine.helpers import KNIGHT_MOVES
from chess_engine.move.move_generator.sliding_move_generator import SlidingMoveGenerator


class KnightMoveGenerator:
    def __init__(self, game_state):
        self.sliding_generator = SlidingMoveGenerator(game_state)

    def generate(self, row, col, possible_moves):
        self.sliding_generator._generate(row, col, KNIGHT_MOVES, possible_moves, 1)