class DeadPositionValidator:
    """
    Detect positions where neither player can possibly deliver checkmate.

    This covers bare kings, a single bishop or knight against a bare king,
    and bishop-only positions where every bishop is confined to the same
    square color. Positions containing pawns, rooks, or queens are not dead.
    """

    def __init__(self, game_state):
        """Bind the validator to the active match state."""
        self.game_state = game_state

    ####################################################################################
    # ---------------------------- DEAD POSITION CHECK --------------------------------
    ####################################################################################

    def is_dead_position(self):
        """Return whether checkmate is impossible from the current position."""
        non_king_pieces = self._get_non_king_pieces()

        if not non_king_pieces:
            return True

        if len(non_king_pieces) == 1:
            return non_king_pieces[0][0][1] in ('B', 'N')

        if all(piece[1] == 'B' for piece, _ in non_king_pieces):
            bishop_square_colors = {
                (row + col) % 2
                for _, (row, col) in non_king_pieces
            }
            return len(bishop_square_colors) == 1

        return False

    ####################################################################################
    # ------------------------------- BOARD HELPERS -----------------------------------
    ####################################################################################

    def _get_non_king_pieces(self):
        """Return `(piece, square)` pairs for every piece except either king."""
        return [
            (piece, (row, col))
            for row, board_row in enumerate(self.game_state.board.board)
            for col, piece in enumerate(board_row)
            if piece[1:] not in ('-', 'K')
        ]
