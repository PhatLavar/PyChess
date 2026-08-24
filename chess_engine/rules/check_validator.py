from chess_engine.utilities import enemy_color, turn_color


class CheckValidator:
    """Evaluate check, checkmate, and stalemate for the active position."""

    def __init__(self, game_state, attack_validator):
        """Bind match state and the shared attack evaluator."""
        self.game_state = game_state
        self.attack_validator = attack_validator

    def find_king(self, color=None):
        """Return the requested king square, defaulting to side to move."""
        if color is None:
            color = turn_color(self.game_state.white_to_move)

        return (
            self.game_state.white_king_position
            if color == 'w'
            else self.game_state.black_king_position
        )

    def in_check(self, color=None):
        """Return whether the requested color's king is currently attacked."""
        if color is None:
            color = turn_color(self.game_state.white_to_move)

        king_position = self.find_king(color)
        enemy = enemy_color(color)

        return self.attack_validator.square_under_attack(king_position, enemy)

    def is_checkmate(self):
        """Return whether side to move is checked and has no legal moves."""
        valid_moves = self.game_state.move.get_valid_moves()
        return len(valid_moves) == 0 and self.in_check()

    def is_stalemate(self):
        """Return whether side to move is safe but has no legal moves."""
        valid_moves = self.game_state.move.get_valid_moves()
        return len(valid_moves) == 0 and not self.in_check()
