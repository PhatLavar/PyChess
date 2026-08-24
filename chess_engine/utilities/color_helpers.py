def enemy_color(color):
    """
    Return `b` for White, or `w` for Black.
    """
    return 'b' if color == 'w' else 'w'


def turn_color(white_to_move):
    """
    Return the piece-color code for the current boolean turn value.
    """
    return 'w' if white_to_move else 'b'
