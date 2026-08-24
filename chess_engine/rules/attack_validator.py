from chess_engine.utilities import (
    DIAGONAL,
    EMP,
    KING_MOVES,
    KNIGHT_MOVES,
    ORTHOGONAL,
    in_bounds,
    piece_color,
    piece_type,
)


class AttackValidator:
    """Determine whether a square is attacked by a specified color."""

    def __init__(self, game_state):
        """Bind the active match state."""
        self.game_state = game_state

    @property
    def board(self):
        """Return the active engine board."""
        return self.game_state.board

    def square_under_attack(self, square, enemy_color):
        """Return whether any enemy pawn, step piece, or slider attacks square."""
        row, col = square

        if self._attacked_by_pawn(row, col, enemy_color):
            return True

        if self._attacked_by_step_piece(row, col, enemy_color, KNIGHT_MOVES, 'N'):
            return True

        if self._attacked_by_step_piece(row, col, enemy_color, KING_MOVES, 'K'):
            return True

        if self._attacked_by_sliding_piece(row, col, enemy_color, ORTHOGONAL, ('R', 'Q')):
            return True

        if self._attacked_by_sliding_piece(row, col, enemy_color, DIAGONAL, ('B', 'Q')):
            return True

        return False

    def _attacked_by_pawn(self, row, col, enemy_color):
        """Return whether an enemy pawn attacks the supplied coordinates."""
        pawn_direction = 1 if enemy_color == 'w' else -1

        for d_col in (-1, 1):
            attack_row = row + pawn_direction
            attack_col = col + d_col

            if in_bounds(attack_row, attack_col, self.board.DIMENSION):
                piece = self.board.get_piece((attack_row, attack_col))
                if piece == enemy_color + 'P':
                    return True

        return False

    def _attacked_by_step_piece(self, row, col, enemy, directions, attacker_type):
        """Return whether a knight-like or king-like attacker reaches square."""
        for d_row, d_col in directions:
            attack_row = row + d_row
            attack_col = col + d_col

            if in_bounds(attack_row, attack_col, self.board.DIMENSION):
                piece = self.board.get_piece((attack_row, attack_col))
                if piece == enemy + attacker_type:
                    return True

        return False

    def _attacked_by_sliding_piece(
        self,
        row,
        col,
        enemy_color,
        directions,
        valid_piece_types
    ):
        """Return whether a rook, bishop, or queen attacks along a ray."""
        for d_row, d_col in directions:
            attack_row = row + d_row
            attack_col = col + d_col

            while in_bounds(attack_row, attack_col, self.board.DIMENSION):
                piece = self.board.get_piece((attack_row, attack_col))

                if piece == EMP:
                    attack_row += d_row
                    attack_col += d_col
                    continue

                if piece_color(piece) == enemy_color and piece_type(piece) in valid_piece_types:
                    return True

                break

        return False
