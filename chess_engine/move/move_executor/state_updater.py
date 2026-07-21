from chess_engine.helpers import EMP, CASTLING_ROOK_START, piece_color


class StateUpdater:
    def __init__(self, game_state):
        self.game_state = game_state


    def reset_click_state(self):
        self.game_state.selected_square = ()
        self.game_state.player_clicked = []


    def update_king_position(self, piece, square):
        if piece == 'wK':
            self.game_state.white_king_position = square
        elif piece == 'bK':
            self.game_state.black_king_position = square


    def clear_en_passant_state(self):
        self.game_state.last_double_pawn_move = None
        self.game_state.en_passant_target = None


    def update_en_passant_state(self, moved_piece, moved_square, target_square):
        self.clear_en_passant_state()

        is_pawn = moved_piece[1] == 'P'
        moved_two_rows = abs(target_square[0] - moved_square[0]) == 2

        if not is_pawn or not moved_two_rows:
            return

        self.game_state.last_double_pawn_move = {
            'pawn': moved_piece,
            'from_square': moved_square,
            'to_square': target_square,
        }

        self.game_state.en_passant_target = (
            (moved_square[0] + target_square[0]) // 2,
            moved_square[1]
        )


    def save_castling_rights_state(self):
        rights_copy = {
            'w': self.game_state.castling_rights['w'].copy(),
            'b': self.game_state.castling_rights['b'].copy(),
        }
        self.game_state.castling_rights_log.append(rights_copy)


    def restore_castling_rights_after_undo(self):
        if not self.game_state.castling_rights_log:
            return

        self.game_state.castling_rights = self.game_state.castling_rights_log.pop()


    def remove_castling_rights_after_move(
        self,
        moved_piece,
        moved_square,
        target_piece,
        target_square
    ):
        color = piece_color(moved_piece)

        if moved_piece[1] == 'K':
            self.game_state.castling_rights[color]['king_side'] = False
            self.game_state.castling_rights[color]['queen_side'] = False

        if moved_piece[1] == 'R':
            self._remove_rook_castling_right(color, moved_square)

        if target_piece != EMP and target_piece[1] == 'R':
            captured_color = piece_color(target_piece)
            self._remove_rook_castling_right(captured_color, target_square)


    def _remove_rook_castling_right(self, color, rook_square):
        if rook_square == CASTLING_ROOK_START[color]['king_side']:
            self.game_state.castling_rights[color]['king_side'] = False
        elif rook_square == CASTLING_ROOK_START[color]['queen_side']:
            self.game_state.castling_rights[color]['queen_side'] = False