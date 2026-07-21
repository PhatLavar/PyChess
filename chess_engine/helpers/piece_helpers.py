from chess_engine.helpers.constants import EMP


def in_bounds(row, col, dimension=8):
    return 0 <= row < dimension and 0 <= col < dimension


def piece_color(piece):
    return None if piece == EMP else piece[0]


def piece_type(piece):
    return None if piece == EMP else piece[1]