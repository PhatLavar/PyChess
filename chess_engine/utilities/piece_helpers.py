from chess_engine.utilities.constants import EMP


def in_bounds(row, col, dimension=8):
    """
    Return whether a row and column are inside a square board.
    """
    return 0 <= row < dimension and 0 <= col < dimension


def piece_color(piece):
    """
    Return `w`, `b`, or `None` for an empty square.
    """
    return None if piece == EMP else piece[0]


def piece_type(piece):
    """
    Return the piece type letter, or `None` for an empty square.
    """
    return None if piece == EMP else piece[1]
