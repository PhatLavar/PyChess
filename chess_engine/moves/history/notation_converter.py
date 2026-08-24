class NotationConverter:
    """Convert internal board coordinates to algebraic square names."""

    def __init__(self, board):
        """Bind the board whose dimension defines rank numbering."""
        self.board = board

    def square_to_notation(self, square):
        """Return notation such as ``e4`` for a ``(row, column)`` square."""
        files = 'abcdefgh'
        row, col = square
        file = files[col]
        rank = str(self.board.DIMENSION - row)
        return f"{file}{rank}"
