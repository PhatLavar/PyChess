import random

from chess_engine.bots.medium_bot import MediumBot
from chess_engine.utilities import EMP, piece_color, piece_type


class HardBot(MediumBot):
    """A deeper alpha-beta bot with a fuller positional evaluation."""

    CASTLED_KING_SQUARES = {
        'w': {(7, 2), (7, 6)},
        'b': {(0, 2), (0, 6)},
    }

    def __init__(self, depth=3, rng=None, choice_window=5):
        """Create the hard bot with a three-ply search by default."""
        super().__init__(
            depth=depth,
            rng=rng or random.Random(),
            choice_window=choice_window,
        )

    def _evaluate(self, game_state, depth_remaining=0):
        score = super()._evaluate(game_state, depth_remaining)
        if game_state.game_over:
            return score

        enemy = 'b' if self.color == 'w' else 'w'
        score += self._positional_score(game_state, self.color)
        score -= self._positional_score(game_state, enemy)

        if game_state.move_validator.in_check():
            checked_color = 'w' if game_state.white_to_move else 'b'
            score += 35 if checked_color != self.color else -35

        return score

    def _positional_score(self, game_state, color):
        score = 0
        pawn_files = [0] * game_state.board.DIMENSION

        for row in range(game_state.board.DIMENSION):
            for col in range(game_state.board.DIMENSION):
                piece = game_state.board.get_piece((row, col))
                if piece == EMP or piece_color(piece) != color:
                    continue

                kind = piece_type(piece)
                if kind == 'P':
                    pawn_files[col] += 1
                    advancement = 6 - row if color == 'w' else row - 1
                    score += max(0, advancement) * 4
                elif kind in {'N', 'B'}:
                    score += self._centralization_bonus(row, col)
                elif kind == 'R' and self._is_open_file(game_state, col):
                    score += 18
                elif kind == 'K' and (row, col) in self.CASTLED_KING_SQUARES[color]:
                    score += 30

        score -= sum(max(0, count - 1) * 18 for count in pawn_files)
        return score

    def _centralization_bonus(self, row, col):
        distance = abs(3.5 - row) + abs(3.5 - col)
        return max(0, int(24 - distance * 5))

    def _is_open_file(self, game_state, col):
        return all(
            piece_type(game_state.board.get_piece((row, col))) != 'P'
            for row in range(game_state.board.DIMENSION)
        )
