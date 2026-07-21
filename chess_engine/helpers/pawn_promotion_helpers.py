from chess_engine.helpers.color_helpers import turn_color


def get_promotion_row(white_to_move):
    return 0 if white_to_move else 7


def get_promotion_color(white_to_move):
    return turn_color(white_to_move)


def get_promotion_piece(white_to_move, chosen_piece):
    turn = turn_color(white_to_move)
    return turn + chosen_piece