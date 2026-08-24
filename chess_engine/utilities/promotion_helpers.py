from chess_engine.utilities.color_helpers import turn_color


def get_promotion_row(white_to_move):
    """
    Return the destination row on which the moving pawn promotes.
    """
    return 0 if white_to_move else 7


def get_promotion_color(white_to_move):
    """
    Return the color code of the pawn that may promote.
    """
    return turn_color(white_to_move)


def get_promotion_piece(white_to_move, chosen_piece):
    """
    Return a full promoted-piece code such as `wQ` or `bN`.
    """
    turn = turn_color(white_to_move)
    return turn + chosen_piece
