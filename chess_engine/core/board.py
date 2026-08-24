from chess_engine.utilities import EMP


class Board:
    """Store and provide access to the current eight-by-eight board position."""

    DIMENSION = 8

    def __init__(self):
        """Create a board in the standard chess starting position."""
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
            [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
            [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
            [EMP, EMP, EMP, EMP, EMP, EMP, EMP, EMP],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]

    def get_piece(self, square):
        """Return the piece code at ``square``, or ``EMP`` when it is empty."""
        row, col = square
        return self.board[row][col]

    def set_piece(self, square, piece):
        """Replace the contents of ``square`` with ``piece``."""
        row, col = square
        self.board[row][col] = piece
