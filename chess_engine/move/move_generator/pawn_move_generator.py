from chess_engine.helpers import (
    EMP,
    enemy_color,
    in_bounds,
    piece_color,
    piece_type,
    turn_color,
)


class PawnMoveGenerator:
    def __init__(self, game_state):
        self.game_state = game_state

    @property
    def board(self):
        return self.game_state.board

    def generate(self, row, col, possible_moves):
        color = turn_color(self.game_state.white_to_move)
        enemy = enemy_color(color)

        direction = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1
        promotion_row = 0 if color == 'w' else 7

        if row == promotion_row:
            return

        self._add_forward_moves(row, col, direction, start_row, possible_moves)
        self._add_capture_moves(row, col, direction, enemy, possible_moves)

    def _add_forward_moves(self, row, col, direction, start_row, possible_moves):
        one_step = (row + direction, col)

        if self.board.get_piece(one_step) != EMP:
            return

        possible_moves.append(((row, col), one_step))

        two_step = (row + direction * 2, col)
        if row == start_row and self.board.get_piece(two_step) == EMP:
            possible_moves.append(((row, col), two_step))

    def _add_capture_moves(self, row, col, direction, enemy, possible_moves):
        for d_col in (-1, 1):
            target = (row + direction, col + d_col)

            if not in_bounds(target[0], target[1], self.board.DIMENSION):
                continue

            if target == self.game_state.en_passant_target:
                possible_moves.append(((row, col), target))

            target_piece = self.board.get_piece(target)

            if piece_color(target_piece) == enemy and piece_type(target_piece) != 'K':
                possible_moves.append(((row, col), target))