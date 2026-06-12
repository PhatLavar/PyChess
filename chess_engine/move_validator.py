class MoveValidator:
    def __init__(self, game_state):
        self.game_state = game_state


    def _find_king(self, color=None):
        pass


    def _get_enemy_color(self):
        pass


    def _is_pinned(self):
        pass


    def _in_check(self):
        pass



    ####################################################################################
    # ---------------------------- CHECKMATE, STALEMATE --------------------------------
    ####################################################################################
    def is_checkmate(self):
        valid_move = self.game_state.move.get_valid_moves()
        return len(valid_move) == 0 and self.in_check()


    def is_stalemate(self):
        valid_move = self.game_state.move.get_valid_moves()
        return len(valid_move) == 0 and not self.in_check()