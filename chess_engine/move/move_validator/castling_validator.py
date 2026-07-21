from chess_engine.helpers import (
    EMP,
    CASTLING_KING_START,
    CASTLING_ROOK_START,
    enemy_color,
)


class CastlingValidator:
    def __init__(self, game_state, attack_validator):
        self.game_state = game_state
        self.attack_validator = attack_validator

    @property
    def board(self):
        return self.game_state.board

    def is_castling_move(self, moved_piece, moved_square, target_square):
        return (
            moved_piece != EMP
            and moved_piece[1] == 'K'
            and abs(target_square[1] - moved_square[1]) == 2
        )

    def can_castle(self, color, side):
        rights = self.game_state.castling_rights[color]

        if not rights[side]:
            return False

        king_start = CASTLING_KING_START[color]
        rook_start = CASTLING_ROOK_START[color][side]

        king = self.board.get_piece(king_start)
        rook = self.board.get_piece(rook_start)

        if king != color + 'K':
            return False

        if rook != color + 'R':
            return False

        if self._in_check(color):
            return False

        if not self._castling_path_empty(color, side):
            return False

        if self._castling_path_under_attack(color, side):
            return False

        return True

    def _in_check(self, color):
        king_position = CASTLING_KING_START[color]
        enemy = enemy_color(color)

        return self.attack_validator.square_under_attack(king_position, enemy)

    def _castling_path_empty(self, color, side):
        row = 7 if color == 'w' else 0

        if side == 'king_side':
            squares = [(row, 5), (row, 6)]
        else:
            squares = [(row, 1), (row, 2), (row, 3)]

        return all(self.board.get_piece(square) == EMP for square in squares)

    def _castling_path_under_attack(self, color, side):
        row = 7 if color == 'w' else 0
        enemy = enemy_color(color)

        if side == 'king_side':
            king_path = [(row, 5), (row, 6)]
        else:
            king_path = [(row, 3), (row, 2)]

        return any(
            self.attack_validator.square_under_attack(square, enemy)
            for square in king_path
        )