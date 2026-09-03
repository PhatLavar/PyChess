class RepetitionTracker:
    """
    Track complete chess positions for automatic threefold-repetition draws.

    Repetition is based on the available moves, not only the visible board.
    The side to move, castling rights, and a legally usable en passant target
    are therefore included in every position key.
    """

    REQUIRED_OCCURRENCES = 3

    def __init__(self, game_state):
        """Bind the match and record its initial position once."""
        self.game_state = game_state
        self.position_history = []
        self.position_counts = {}
        self.record_current_position()

    ####################################################################################
    # ------------------------------ POSITION LIFECYCLE --------------------------------
    ####################################################################################

    def record_current_position(self):
        """Record the current position and return its occurrence count."""
        position_key = self._build_position_key()
        self.position_history.append(position_key)
        self.position_counts[position_key] = (
            self.position_counts.get(position_key, 0) + 1
        )
        return self.position_counts[position_key]

    def remove_current_position(self):
        """Remove the latest position when its producing move is undone."""
        if len(self.position_history) <= 1:
            return

        position_key = self.position_history.pop()
        remaining = self.position_counts[position_key] - 1

        if remaining == 0:
            del self.position_counts[position_key]
        else:
            self.position_counts[position_key] = remaining

    ####################################################################################
    # ------------------------------- POSITION IDENTITY --------------------------------
    ####################################################################################

    def _build_position_key(self):
        """Return an immutable identity for the current legal position."""
        board_key = tuple(
            piece
            for row in self.game_state.board.board
            for piece in row
        )
        rights = self.game_state.castling_rights
        castling_key = (
            rights['w']['king_side'],
            rights['w']['queen_side'],
            rights['b']['king_side'],
            rights['b']['queen_side'],
        )
        return (
            board_key,
            self.game_state.white_to_move,
            castling_key,
            self._get_effective_en_passant_target(),
        )

    def _get_effective_en_passant_target(self):
        """Return the en passant target only when a legal capture exists."""
        target = self.game_state.en_passant_target
        if target is None:
            return None

        for origin, move_target in self.game_state.move.get_valid_moves():
            if (
                move_target == target
                and self.game_state.board.get_piece(origin)[1:] == 'P'
            ):
                return target
        return None
