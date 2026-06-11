class MoveValidator:
    def __init__(self, game_state):
        self.game_state = game_state


    def _find_king(self):
        return self.game_state.white_king_location if self.game_state.white_to_move else self.game_state.black_king_location


    def in_check(self):
        king_position = self._find_king()

        self.game_state.white_to_move = not self.game_state.white_to_move
        opponent_moves = self.game_state.move.get_all_possible_moves()

        self.game_state.white_to_move = not self.game_state.white_to_move
        for move in opponent_moves:
            target_square = move[1]
            if target_square == king_position:
                return True

        return False


    def is_checkmate(self):
        valid_move = self.game_state.get_valid_moves()
        return len(valid_move) == 0 and self.in_check()


    def is_stalemate(self):
        valid_move = self.game_state.get_valid_moves()
        return len(valid_move) == 0 and not self.in_check()