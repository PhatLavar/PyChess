from chess_engine.helpers import EMP


class EnPassantValidator:
    def __init__(self, game_state):
        self.game_state = game_state

    @property
    def board(self):
        return self.game_state.board

    def is_en_passant_move(self, moved_piece, moved_square, target_square):
        return (
            moved_piece[1] == 'P'
            and target_square == self.game_state.en_passant_target
            and self.board.get_piece(target_square) == EMP
            and moved_square[1] != target_square[1]
            and self.game_state.last_double_pawn_move is not None
        )