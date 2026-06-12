class MoveValidator:
    def __init__(self, game_state):
        self.game_state = game_state


    def _find_king(self, color=None):
        if color is None:
            color = 'w' if self.game_state.white_to_move else 'b'

        return self.game_state.white_king_position if color == 'w' else self.game_state.black_king_position


    def _get_enemy_color(self, color=None):
        if color is None:
            color = 'w' if self.game_state.white_to_move else 'b'

        return 'b' if color == 'w' else 'w'


    def _in_bounds(self, row, col):
        return 0 <= row < self.game_state.board.DIMENSION and 0 <= col < self.game_state.board.DIMENSION


    def _square_under_attack(self, square, enemy_color):
        row, col = square

        pawn_direction = 1 if enemy_color == 'w' else -1
        for d_col in (-1, 1):
            attack_row = row + pawn_direction
            attack_col = col + d_col
            if self._in_bounds(attack_row, attack_col):
                piece = self.game_state.board.board[attack_row][attack_col]
                if piece == enemy_color + 'P':
                    return True

        knight_directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for d_row, d_col in knight_directions:
            attack_row = row + d_row
            attack_col = col + d_col
            if self._in_bounds(attack_row, attack_col):
                piece = self.game_state.board.board[attack_row][attack_col]
                if piece == enemy_color + 'N':
                    return True

        king_directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]
        for d_row, d_col in king_directions:
            attack_row = row + d_row
            attack_col = col + d_col
            if self._in_bounds(attack_row, attack_col):
                piece = self.game_state.board.board[attack_row][attack_col]
                if piece == enemy_color + 'K':
                    return True

        straight_directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        if self._attacked_by_sliding_piece(row, col, enemy_color, straight_directions, ('R', 'Q')):
            return True

        diagonal_directions = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
        if self._attacked_by_sliding_piece(row, col, enemy_color, diagonal_directions, ('B', 'Q')):
            return True

        return False


    def _attacked_by_sliding_piece(self, row, col, enemy_color, directions, valid_piece_types):
        for d_row, d_col in directions:
            attack_row = row + d_row
            attack_col = col + d_col

            while self._in_bounds(attack_row, attack_col):
                piece = self.game_state.board.board[attack_row][attack_col]

                if piece == '--':
                    attack_row += d_row
                    attack_col += d_col
                    continue

                if piece[0] == enemy_color and piece[1] in valid_piece_types:
                    return True

                break

        return False


    def _is_pinned(self, square, color=None):
        if color is None:
            color = 'w' if self.game_state.white_to_move else 'b'

        row, col = square
        piece = self.game_state.board.board[row][col]
        if piece == '--' or piece[0] != color or piece[1] == 'K':
            return False

        self.game_state.board.board[row][col] = '--'
        is_pinned = self._in_check(color)
        self.game_state.board.board[row][col] = piece

        return is_pinned


    def _in_check(self, color=None):
        if color is None:
            color = 'w' if self.game_state.white_to_move else 'b'

        king_position = self._find_king(color)
        enemy_color = self._get_enemy_color(color)
        return self._square_under_attack(king_position, enemy_color)


    def in_check(self, color=None):
        return self._in_check(color)



    ####################################################################################
    # ---------------------------- CHECKMATE, STALEMATE --------------------------------
    ####################################################################################
    def is_checkmate(self):
        valid_move = self.game_state.move.get_valid_moves()
        return len(valid_move) == 0 and self._in_check()


    def is_stalemate(self):
        valid_move = self.game_state.move.get_valid_moves()
        return len(valid_move) == 0 and not self._in_check()
