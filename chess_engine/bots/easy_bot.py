import random

from chess_engine.bots.base import BaseBot
from chess_engine.utilities import EMP, piece_type


class EasyBot(BaseBot):
    """A lightweight bot that favors captures and natural development.

    The bot looks only at the current move. Random choice among similarly
    scored moves keeps its play varied and intentionally beatable.
    """

    PIECE_VALUES = {
        'P': 100,
        'N': 320,
        'B': 330,
        'R': 500,
        'Q': 900,
        'K': 0,
    }
    CENTER_SQUARES = {(3, 3), (3, 4), (4, 3), (4, 4)}
    EXTENDED_CENTER = {
        (2, 2), (2, 3), (2, 4), (2, 5),
        (3, 2), (3, 5), (4, 2), (4, 5),
        (5, 2), (5, 3), (5, 4), (5, 5),
    }
    DEVELOPMENT_SQUARES = {
        'w': {(7, 1), (7, 2), (7, 5), (7, 6)},
        'b': {(0, 1), (0, 2), (0, 5), (0, 6)},
    }

    def __init__(self, rng=None, choice_window=25):
        """Create the bot with an optional seeded random number generator."""
        self.rng = rng or random.Random()
        self.choice_window = choice_window

    def choose_move(self, game_state):
        """Choose one legal move without changing ``game_state``."""
        valid_moves = game_state.move.get_valid_moves()
        if not valid_moves:
            return None

        scored_moves = [
            (self.score_move(game_state, move), move)
            for move in valid_moves
        ]
        best_score = max(score for score, _ in scored_moves)
        candidates = [
            move for score, move in scored_moves
            if score >= best_score - self.choice_window
        ]
        return self.rng.choice(candidates)

    def score_move(self, game_state, move):
        """Return the easy bot's shallow preference score for ``move``."""
        origin, target = move
        board = game_state.board
        moved_piece = board.get_piece(origin)
        target_piece = board.get_piece(target)
        score = self.rng.randint(0, 10)

        if target_piece != EMP:
            score += self.PIECE_VALUES[piece_type(target_piece)]

        if target in self.CENTER_SQUARES:
            score += 30
        elif target in self.EXTENDED_CENTER:
            score += 12

        color = moved_piece[0]
        if (
            origin in self.DEVELOPMENT_SQUARES[color]
            and piece_type(moved_piece) in {'N', 'B'}
        ):
            score += 20

        if piece_type(moved_piece) == 'P' and target[0] in {0, 7}:
            score += self.PIECE_VALUES['Q']

        return score
