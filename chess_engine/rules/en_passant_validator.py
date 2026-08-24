from chess_engine.utilities import EMP


class EnPassantValidator:
    """Recognize en passant moves from the current transient match state."""

    def __init__(self, game_state):
        """Bind the active match state."""
        self.game_state = game_state

    @property
    def board(self):
        """Return the active engine board."""
        return self.game_state.board

    def is_en_passant_move(self, moved_piece, moved_square, target_square):
        """Return whether the supplied pawn move is a legal en passant shape."""
        return (
            moved_piece[1] == 'P'
            and target_square == self.game_state.en_passant_target
            and self.board.get_piece(target_square) == EMP
            and moved_square[1] != target_square[1]
            and self.game_state.last_double_pawn_move is not None
        )
