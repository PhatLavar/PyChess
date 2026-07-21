from chess_engine.helpers import EMP


class MoveSimulation:
    def __init__(self, game_state):
        self.game_state = game_state

    @property
    def board(self):
        return self.game_state.board

    def simulate(self, move):
        moved_square, target_square = move
        moved_piece = self.board.get_piece(moved_square)
        target_piece = self.board.get_piece(target_square)

        en_passant_capture_square = None
        en_passant_captured_piece = None

        if self.game_state.move_validator.is_en_passant_move(
            moved_piece,
            moved_square,
            target_square
        ):
            en_passant_capture_square = self.game_state.last_double_pawn_move['to_square']
            en_passant_captured_piece = self.board.get_piece(en_passant_capture_square)

        state = {
            'moved_square': moved_square,
            'target_square': target_square,
            'moved_piece': moved_piece,
            'target_piece': target_piece,
            'en_passant_capture_square': en_passant_capture_square,
            'en_passant_captured_piece': en_passant_captured_piece,
            'white_king_position': self.game_state.white_king_position,
            'black_king_position': self.game_state.black_king_position,
        }

        self.board.set_piece(target_square, moved_piece)
        self.board.set_piece(moved_square, EMP)

        if en_passant_capture_square is not None:
            self.board.set_piece(en_passant_capture_square, EMP)

        self._update_king_position(moved_piece, target_square)

        return state

    def restore(self, state):
        self.board.set_piece(state['moved_square'], state['moved_piece'])
        self.board.set_piece(state['target_square'], state['target_piece'])

        if state['en_passant_capture_square'] is not None:
            self.board.set_piece(
                state['en_passant_capture_square'],
                state['en_passant_captured_piece']
            )

        self.game_state.white_king_position = state['white_king_position']
        self.game_state.black_king_position = state['black_king_position']

    def _update_king_position(self, piece, square):
        if piece == 'wK':
            self.game_state.white_king_position = square
        elif piece == 'bK':
            self.game_state.black_king_position = square