from chess_engine.utilities import (
    KING_MOVES,
    CASTLING_KING_START,
    CASTLING_KING_TARGET,
    turn_color,
)
from chess_engine.moves.generation.sliding_move_generator import SlidingMoveGenerator


class KingMoveGenerator:
    """Generate one-square king moves and eligible castling moves."""

    def __init__(self, game_state):
        """Bind state and reuse the directional generator for king steps."""
        self.game_state = game_state
        self.sliding_generator = SlidingMoveGenerator(game_state)

    def generate(self, row, col, possible_moves):
        """Append pseudo-legal king moves from the supplied square."""
        self.sliding_generator._generate(row, col, KING_MOVES, possible_moves, 1)
        self._add_castling_moves(row, col, possible_moves)

    def _add_castling_moves(self, row, col, possible_moves):
        """Append legal king- and queen-side castling destinations."""
        color = turn_color(self.game_state.white_to_move)

        if (row, col) != CASTLING_KING_START[color]:
            return

        validator = self.game_state.move_validator

        if validator.can_castle(color, 'king_side'):
            possible_moves.append(((row, col), CASTLING_KING_TARGET[color]['king_side']))

        if validator.can_castle(color, 'queen_side'):
            possible_moves.append(((row, col), CASTLING_KING_TARGET[color]['queen_side']))
