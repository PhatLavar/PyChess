EMP = '--'

ORTHOGONAL = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIAGONAL = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
KING_MOVES = ORTHOGONAL + DIAGONAL
KNIGHT_MOVES = [
    (-2, -1), (-2, 1),
    (-1, -2), (-1, 2),
    (1, -2), (1, 2),
    (2, -1), (2, 1)
]

CASTLING_KING_START = {
    'w': (7, 4),
    'b': (0, 4),
}

CASTLING_ROOK_START = {
    'w': {
        'king_side': (7, 7),
        'queen_side': (7, 0),
    },
    'b': {
        'king_side': (0, 7),
        'queen_side': (0, 0),
    },
}

CASTLING_KING_TARGET = {
    'w': {
        'king_side': (7, 6),
        'queen_side': (7, 2),
    },
    'b': {
        'king_side': (0, 6),
        'queen_side': (0, 2),
    },
}

CASTLING_ROOK_TARGET = {
    'w': {
        'king_side': (7, 5),
        'queen_side': (7, 3),
    },
    'b': {
        'king_side': (0, 5),
        'queen_side': (0, 3),
    },
}