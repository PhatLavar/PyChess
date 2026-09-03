class FiftyMoveRule:
    """
    Track progress toward the fifty-move draw.

    Chess counts one move by either player as a half-move. The draw becomes
    available after 100 consecutive half-moves without a pawn move or capture.
    PyChess applies that draw automatically.
    """

    REQUIRED_HALF_MOVES = 100

    def __init__(self):
        """Create a fresh counter and an empty undo history."""
        self.halfmove_clock = 0
        self.clock_history = []

    ####################################################################################
    # ------------------------------- MOVE TRACKING -----------------------------------
    ####################################################################################

    def record_move(self, moved_piece, is_capture):
        """Update the counter after a completed move."""
        self.clock_history.append(self.halfmove_clock)

        if moved_piece[1] == 'P' or is_capture:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

    def undo_move(self):
        """Restore the counter value from before the latest move."""
        if self.clock_history:
            self.halfmove_clock = self.clock_history.pop()

    def is_draw(self):
        """Return whether 100 qualifying half-moves have been completed."""
        return self.halfmove_clock >= self.REQUIRED_HALF_MOVES
