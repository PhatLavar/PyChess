"""Shared chess constants and small pure helper functions."""

from chess_engine.utilities.color_helpers import enemy_color, turn_color
from chess_engine.utilities.constants import (
    CASTLING_KING_START,
    CASTLING_KING_TARGET,
    CASTLING_ROOK_START,
    CASTLING_ROOK_TARGET,
    DIAGONAL,
    EMP,
    KING_MOVES,
    KNIGHT_MOVES,
    ORTHOGONAL,
)
from chess_engine.utilities.piece_helpers import in_bounds, piece_color, piece_type
from chess_engine.utilities.promotion_helpers import (
    get_promotion_color,
    get_promotion_row,
)

__all__ = [
    'CASTLING_KING_START',
    'CASTLING_KING_TARGET',
    'CASTLING_ROOK_START',
    'CASTLING_ROOK_TARGET',
    'DIAGONAL',
    'EMP',
    'KING_MOVES',
    'KNIGHT_MOVES',
    'ORTHOGONAL',
    'enemy_color',
    'get_promotion_color',
    'get_promotion_row',
    'in_bounds',
    'piece_color',
    'piece_type',
    'turn_color',
]
