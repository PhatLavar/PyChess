from chess_engine.moves.execution.state_updater import StateUpdater
from chess_engine.utilities import EMP, piece_color


class PawnPromotionExecutor:
    """Store pending promotion state and apply the chosen piece."""

    def __init__(self, game_state, move_logger):
        """Bind match state and move history."""
        self.game_state = game_state
        self.move_logger = move_logger
        self.state_updater = StateUpdater(game_state)


    @property
    def board(self):
        """Return the active engine board."""
        return self.game_state.board


    def set_pending_state(self, moved_piece, moved_square, target_piece, target_square):
        """Pause a pawn move until the application supplies a piece choice."""
        self.game_state.promotion_pending = True
        self.game_state.promotion_square = target_square
        self.game_state.promotion_moved_square = moved_square
        self.game_state.promotion_moved_piece = moved_piece
        self.game_state.promotion_target_piece = target_piece
        self.game_state.promotion_color = piece_color(moved_piece)


    def execute(self, chosen_type):
        """Complete and record a pending promotion."""
        moved_piece = self.game_state.promotion_moved_piece
        moved_square = self.game_state.promotion_moved_square
        target_piece = self.game_state.promotion_target_piece
        target_square = self.game_state.promotion_square
        promoted_piece = self.game_state.promotion_color + chosen_type
        is_capture = target_piece != EMP

        self.state_updater.save_castling_rights_state()
        self.state_updater.remove_castling_rights_after_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square
        )

        self.board.set_piece(target_square, promoted_piece)
        self.board.set_piece(moved_square, EMP)

        self.move_logger.save_promotion_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square,
            is_capture,
            promotion_piece=promoted_piece
        )

        self._clear_promotion_state()
        self.state_updater.clear_en_passant_state()
        move_status, match_result = self.game_state.finish_turn()
        self.move_logger.record_promotion_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square,
            promoted_piece,
            move_type=move_status or 'PROMOTION'
        )

        if match_result is not None:
            self.move_logger.record_end_match(match_result)

    def _clear_promotion_state(self):
        """Remove every transient promotion field after completion or undo."""
        self.game_state.promotion_pending = False
        self.game_state.promotion_square = None
        self.game_state.promotion_moved_square = None
        self.game_state.promotion_moved_piece = None
        self.game_state.promotion_target_piece = None
        self.game_state.promotion_color = None
