from chess_engine.helpers import EMP
from chess_engine.move.move_executor.state_updater import StateUpdater


class UndoExecutor:
    def __init__(self, game_state, move_logger):
        self.game_state = game_state
        self.move_logger = move_logger
        self.state_updater = StateUpdater(game_state)

    @property
    def board(self):
        return self.game_state.board

    def execute(self):
        if self.game_state.promotion_pending:
            self._clear_promotion_state()
            self.state_updater.reset_click_state()
            return

        if len(self.move_logger.notation) == 0:
            return

        last_move = self.move_logger.notation.pop()

        moved_square = last_move['moved_square']
        target_square = last_move['target_square']
        moved_piece = last_move['moved_piece']
        target_prev_piece = last_move['target_piece']

        if last_move.get('en_passant'):
            self._undo_en_passant(
                moved_square,
                target_square,
                moved_piece,
                target_prev_piece,
                last_move
            )
        elif last_move.get('castling'):
            self._undo_castling(
                moved_square,
                target_square,
                moved_piece,
                last_move
            )
        else:
            self._undo_normal_or_promotion(
                moved_square,
                target_square,
                moved_piece,
                target_prev_piece
            )

        self._restore_en_passant_state_after_undo()
        self.state_updater.restore_castling_rights_after_undo()
        self.state_updater.update_king_position(moved_piece, moved_square)

        if len(self.move_logger.move_log) > 0:
            self.move_logger.move_log.pop()

        self._record_undo_log(last_move, moved_piece, moved_square, target_square, target_prev_piece)

        self.state_updater.reset_click_state()
        self.game_state.white_to_move = not self.game_state.white_to_move

    def _undo_en_passant(
        self,
        moved_square,
        target_square,
        moved_piece,
        target_prev_piece,
        last_move
    ):
        self.board.set_piece(moved_square, moved_piece)
        self.board.set_piece(target_square, EMP)
        self.board.set_piece(
            last_move['en_passant_capture_square'],
            target_prev_piece
        )

    def _undo_castling(self, moved_square, target_square, moved_piece, last_move):
        self.board.set_piece(moved_square, moved_piece)
        self.board.set_piece(target_square, EMP)
        self.board.set_piece(last_move['rook_square'], last_move['rook_piece'])
        self.board.set_piece(last_move['rook_target_square'], EMP)

    def _undo_normal_or_promotion(
        self,
        moved_square,
        target_square,
        moved_piece,
        target_prev_piece
    ):
        self.board.set_piece(moved_square, moved_piece)
        self.board.set_piece(target_square, target_prev_piece)

    def _record_undo_log(
        self,
        last_move,
        moved_piece,
        moved_square,
        target_square,
        target_prev_piece
    ):
        if last_move.get('en_passant'):
            self.move_logger.record_en_passant_undo(
                moved_piece,
                target_square,
                moved_square,
                target_prev_piece,
                last_move['en_passant_capture_square']
            )
        elif last_move.get('castling'):
            self.move_logger.record_castling_undo(
                moved_piece,
                target_square,
                moved_square,
                last_move['castling_side']
            )
        else:
            self.move_logger.record_move(
                moved_piece,
                target_square,
                target_prev_piece,
                moved_square,
                move_type='UNDO'
            )

    def _restore_en_passant_state_after_undo(self):
        self.state_updater.clear_en_passant_state()

        if len(self.move_logger.notation) == 0:
            return

        previous_move = self.move_logger.notation[-1]
        moved_piece = previous_move['moved_piece']
        moved_square = previous_move['moved_square']
        target_square = previous_move['target_square']

        if moved_piece[1] != 'P':
            return

        if abs(target_square[0] - moved_square[0]) != 2:
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

    def _clear_promotion_state(self):
        self.game_state.promotion_pending = False
        self.game_state.promotion_square = None
        self.game_state.promotion_moved_square = None
        self.game_state.promotion_moved_piece = None
        self.game_state.promotion_target_piece = None
        self.game_state.promotion_color = None