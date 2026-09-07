import random

from chess_engine.bots.hard_bot import HardBot
from chess_engine.utilities import EMP, piece_color, piece_type


class MasterBot(HardBot):
    """A deterministic positional bot with tactical capture extensions."""

    def __init__(self, depth=2, quiescence_depth=2, rng=None):
        """Create the master bot with no near-best move randomness."""
        super().__init__(
            depth=depth,
            rng=rng or random.Random(),
            choice_window=0,
        )
        self.quiescence_depth = max(0, quiescence_depth)

    def _minimax(self, game_state, depth, alpha, beta):
        if depth == 0 and not game_state.game_over:
            return self._quiescence(
                game_state,
                alpha,
                beta,
                self.quiescence_depth,
            )
        return super()._minimax(game_state, depth, alpha, beta)

    def _quiescence(self, game_state, alpha, beta, depth):
        """Search captures, or all check evasions, within the depth limit."""
        stand_pat = self._evaluate(game_state)
        if depth == 0 or game_state.game_over:
            return stand_pat

        in_check = game_state.move_validator.in_check()
        moves = [
            move for move in game_state.move.get_valid_moves()
            if in_check or self._is_capture(game_state, move)
        ]
        if not moves:
            return stand_pat

        maximizing = piece_color_for_turn(game_state) == self.color
        moves = self._ordered_moves(game_state, moves)

        if maximizing:
            value = float('-inf') if in_check else stand_pat
            alpha = max(alpha, value)
            for move in moves:
                if alpha >= beta:
                    break
                child = self._state_after_move(game_state, move)
                value = max(
                    value,
                    self._quiescence(child, alpha, beta, depth - 1),
                )
                alpha = max(alpha, value)
            return value

        value = float('inf') if in_check else stand_pat
        beta = min(beta, value)
        for move in moves:
            if alpha >= beta:
                break
            child = self._state_after_move(game_state, move)
            value = min(
                value,
                self._quiescence(child, alpha, beta, depth - 1),
            )
            beta = min(beta, value)
        return value

    def _evaluate(self, game_state, depth_remaining=0):
        score = super()._evaluate(game_state, depth_remaining)
        if game_state.game_over:
            return score

        enemy = 'b' if self.color == 'w' else 'w'
        score += self._strategic_score(game_state, self.color)
        score -= self._strategic_score(game_state, enemy)
        return score

    def _strategic_score(self, game_state, color):
        bishops = 0
        score = 0

        for row in range(game_state.board.DIMENSION):
            for col in range(game_state.board.DIMENSION):
                piece = game_state.board.get_piece((row, col))
                if piece_color(piece) != color:
                    continue

                kind = piece_type(piece)
                if kind == 'B':
                    bishops += 1
                elif kind == 'P':
                    if self._is_passed_pawn(game_state, color, row, col):
                        score += 25
                    if self._is_isolated_pawn(game_state, color, col):
                        score -= 12
                elif kind == 'K':
                    score += self._pawn_shield_score(
                        game_state,
                        color,
                        row,
                        col,
                    )

        if bishops >= 2:
            score += 28
        return score

    def _is_capture(self, game_state, move):
        moved_square, target_square = move
        target_piece = game_state.board.get_piece(target_square)
        moved_piece = game_state.board.get_piece(moved_square)
        return (
            target_piece != EMP
            or (
                piece_type(moved_piece) == 'P'
                and target_square == game_state.en_passant_target
            )
        )

    def _is_passed_pawn(self, game_state, color, row, col):
        enemy = 'b' if color == 'w' else 'w'
        direction = -1 if color == 'w' else 1
        scan_row = row + direction

        while 0 <= scan_row < game_state.board.DIMENSION:
            for scan_col in range(max(0, col - 1), min(7, col + 1) + 1):
                if game_state.board.get_piece((scan_row, scan_col)) == enemy + 'P':
                    return False
            scan_row += direction
        return True

    def _is_isolated_pawn(self, game_state, color, col):
        adjacent_files = [candidate for candidate in (col - 1, col + 1) if 0 <= candidate < 8]
        return not any(
            game_state.board.get_piece((row, adjacent_col)) == color + 'P'
            for adjacent_col in adjacent_files
            for row in range(game_state.board.DIMENSION)
        )

    def _pawn_shield_score(self, game_state, color, row, col):
        direction = -1 if color == 'w' else 1
        shield_row = row + direction
        if not 0 <= shield_row < game_state.board.DIMENSION:
            return 0
        return sum(
            7
            for shield_col in range(max(0, col - 1), min(7, col + 1) + 1)
            if game_state.board.get_piece((shield_row, shield_col)) == color + 'P'
        )


def piece_color_for_turn(game_state):
    """Return the color whose turn is stored in ``game_state``."""
    return 'w' if game_state.white_to_move else 'b'
