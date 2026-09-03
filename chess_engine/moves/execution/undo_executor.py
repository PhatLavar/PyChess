from chess_engine.moves.execution.state_updater import StateUpdater
from chess_engine.utilities import EMP


class UndoExecutor:
    """
    Restore the engine position preceding the latest completed move.
    """

    def __init__(self, game_state, move_logger):
        """
        Bind match state and move history.
        """
        self.game_state = game_state
        self.move_logger = move_logger
        self.state_updater = StateUpdater(game_state)

    @property
    def board(self):
        """
        Return the active engine board.
        """
        return self.game_state.board

    def execute(self):
        """
        Undo pending promotion or latest move; return whether state changed.
        """
        if self.game_state.promotion_pending:
            self._clear_promotion_state()
            return True

        if len(self.move_logger.notation) == 0:
            return False

        self.game_state.repetition_tracker.remove_current_position()
        self.game_state.fifty_move_rule.undo_move()
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

        self.game_state.white_to_move = not self.game_state.white_to_move
        return True

    def _undo_en_passant(
        self,
        moved_square,
        target_square,
        moved_piece,
        target_prev_piece,
        last_move
    ):
        """
        Restore both pawns from an en passant history record.
        """
        self.board.set_piece(moved_square, moved_piece)
        self.board.set_piece(target_square, EMP)
        self.board.set_piece(
            last_move['en_passant_capture_square'],
            target_prev_piece
        )

    def _undo_castling(self, moved_square, target_square, moved_piece, last_move):
        """
        Restore king and rook to their pre-castling squares.
        """
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
        """
        Restore an ordinary move, capture, or promotion.
        """
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
        """
        Append a human-readable undo entry matching the move type.
        """
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
        """
        Reconstruct en passant availability from the new latest move.
        """
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
        """
        Cancel every transient pending-promotion field.
        """
        self.game_state.promotion_pending = False
        self.game_state.promotion_square = None
        self.game_state.promotion_moved_square = None
        self.game_state.promotion_moved_piece = None
        self.game_state.promotion_target_piece = None
        self.game_state.promotion_color = None
