from chess_engine.moves.generation.sliding_move_generator import SlidingMoveGenerator
from chess_engine.utilities import KNIGHT_MOVES


class KnightMoveGenerator:
    """Generate fixed-offset knight moves."""

    def __init__(self, game_state):
        """Reuse the one-step directional generator for knight offsets."""
        self.sliding_generator = SlidingMoveGenerator(game_state)

    def generate(self, row, col, possible_moves):
        """Append pseudo-legal knight moves from the supplied square."""
        self.sliding_generator._generate(row, col, KNIGHT_MOVES, possible_moves, 1)
