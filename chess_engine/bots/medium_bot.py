from copy import deepcopy
import random

from chess_engine.bots.base import BaseBot
from chess_engine.moves.execution.move_executor import MoveExecutor
from chess_engine.utilities import EMP, piece_color, piece_type, turn_color


class MediumBot(BaseBot):
    """A two-ply material and positional bot using alpha-beta search."""

    CHECKMATE_SCORE = 100_000
    PIECE_VALUES = {
        'P': 100,
        'N': 320,
        'B': 330,
        'R': 500,
        'Q': 900,
        'K': 0,
    }
    CENTER_SQUARES = {(3, 3), (3, 4), (4, 3), (4, 4)}

    def __init__(self, depth=2, rng=None, choice_window=15):
        """Create a configurable shallow-search bot."""
        self.depth = max(1, depth)
        self.rng = rng or random.Random()
        self.choice_window = choice_window
        self.color = None

    def choose_move(self, game_state):
        """Return a strong legal move found by a shallow alpha-beta search."""
        valid_moves = game_state.move.get_valid_moves()
        if not valid_moves:
            return None

        self.color = turn_color(game_state.white_to_move)
        scored_moves = []
        for move in self._ordered_moves(game_state, valid_moves):
            child = self._state_after_move(game_state, move)
            # Candidate selection needs exact scores, not cutoff bounds.
            score = self._minimax(
                child, self.depth - 1, float('-inf'), float('inf')
            )
            scored_moves.append((score, move))

        best_score = max(score for score, _ in scored_moves)
        candidates = [
            move for score, move in scored_moves
            if score >= best_score - self.choice_window
        ]
        return self.rng.choice(candidates)

    def _minimax(self, game_state, depth, alpha, beta):
        if depth == 0 or game_state.game_over:
            return self._evaluate(game_state, depth)

        valid_moves = game_state.move.get_valid_moves()
        if not valid_moves:
            return self._evaluate(game_state, depth)

        maximizing = turn_color(game_state.white_to_move) == self.color
        ordered_moves = self._ordered_moves(game_state, valid_moves)

        if maximizing:
            value = float('-inf')
            for move in ordered_moves:
                child = self._state_after_move(game_state, move)
                value = max(value, self._minimax(child, depth - 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value

        value = float('inf')
        for move in ordered_moves:
            child = self._state_after_move(game_state, move)
            value = min(value, self._minimax(child, depth - 1, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

    def _evaluate(self, game_state, depth_remaining=0):
        if game_state.game_over:
            if game_state.winner is None:
                return 0
            bot_won = game_state.winner.startswith(
                'WHITE' if self.color == 'w' else 'BLACK'
            )
            distance_bonus = max(0, depth_remaining)
            return (
                self.CHECKMATE_SCORE + distance_bonus
                if bot_won
                else -self.CHECKMATE_SCORE - distance_bonus
            )

        score = 0
        for row in range(game_state.board.DIMENSION):
            for col in range(game_state.board.DIMENSION):
                piece = game_state.board.get_piece((row, col))
                if piece == EMP:
                    continue

                value = self.PIECE_VALUES[piece_type(piece)]
                if (row, col) in self.CENTER_SQUARES:
                    value += 15
                if piece_type(piece) in {'N', 'B'}:
                    value += self._development_bonus(piece, row)

                score += value if piece_color(piece) == self.color else -value
        return score

    def _development_bonus(self, piece, row):
        home_row = 7 if piece_color(piece) == 'w' else 0
        return 0 if row == home_row else 10

    def _ordered_moves(self, game_state, moves):
        """Search captures first to improve alpha-beta pruning."""
        return sorted(
            moves,
            key=lambda move: self._move_order_score(game_state, move),
            reverse=True,
        )

    def _move_order_score(self, game_state, move):
        moved_square, target_square = move
        moved_piece = game_state.board.get_piece(moved_square)
        target_piece = game_state.board.get_piece(target_square)
        score = 0
        if target_piece != EMP:
            score += (
                10 * self.PIECE_VALUES[piece_type(target_piece)]
                - self.PIECE_VALUES[piece_type(moved_piece)]
            )
        if target_square in self.CENTER_SQUARES:
            score += 20
        return score

    def _state_after_move(self, game_state, move):
        """Return an independent state with one legal move applied."""
        child = deepcopy(game_state)
        child.move.logger.record_logger._append_log = (
            child.move.move_log.append
        )
        outcome = child.move.handle_piece_move(*move)
        if outcome == MoveExecutor.PROMOTION_PENDING:
            child.move.executor.handle_pawn_promotion('Q')
        return child
