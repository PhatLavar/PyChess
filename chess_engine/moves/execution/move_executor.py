from chess_engine.moves.execution.castling_executor import CastlingExecutor
from chess_engine.moves.execution.en_passant_executor import EnPassantExecutor
from chess_engine.moves.execution.normal_executor import NormalMoveExecutor
from chess_engine.moves.execution.promotion_executor import PawnPromotionExecutor
from chess_engine.moves.execution.undo_executor import UndoExecutor
from chess_engine.utilities import EMP, piece_color


class MoveExecutor:
    """Validate requested moves and delegate them to the correct executor."""

    MOVED = 'moved'
    INVALID = 'invalid'
    SAME_COLOR = 'same_color'
    PROMOTION_PENDING = 'promotion_pending'
    BLOCKED = 'blocked'

    def __init__(self, game_state, move_generator, move_logger):
        """Create specialized executors that share state and history."""
        self.game_state = game_state
        self.move_generator = move_generator
        self.move_logger = move_logger

        self.normal_executor = NormalMoveExecutor(game_state, move_logger)
        self.promotion_executor = PawnPromotionExecutor(game_state, move_logger)
        self.en_passant_executor = EnPassantExecutor(game_state, move_logger)
        self.castling_executor = CastlingExecutor(game_state, move_logger)
        self.undo_executor = UndoExecutor(game_state, move_logger)

    @property
    def board(self):
        """Return the active engine board."""
        return self.game_state.board

    def handle_piece_move(self, moved_square, target_square):
        """Attempt a move and return a named outcome for the application layer."""
        if self.game_state.game_over:
            return self.BLOCKED

        moved_piece = self.board.get_piece(moved_square)
        target_piece = self.board.get_piece(target_square)

        if moved_piece == EMP:
            return self.INVALID

        if self._is_same_color_target(moved_piece, target_piece):
            return self.SAME_COLOR

        if (moved_square, target_square) not in self.move_generator.get_valid_moves():
            return self.INVALID

        validator = self.game_state.move_validator

        if validator.is_en_passant_move(moved_piece, moved_square, target_square):
            self.en_passant_executor.execute(moved_piece, moved_square, target_square)
            return self.MOVED

        if moved_piece[1] == 'P' and validator.can_pawn_promotion(target_square):
            self.promotion_executor.set_pending_state(
                moved_piece,
                moved_square,
                target_piece,
                target_square
            )
            return self.PROMOTION_PENDING

        if validator.is_castling_move(moved_piece, moved_square, target_square):
            self.castling_executor.execute(moved_piece, moved_square, target_square)
            return self.MOVED

        self.normal_executor.execute(
            moved_piece,
            moved_square,
            target_piece,
            target_square
        )
        return self.MOVED

    def handle_pawn_promotion(self, chosen_type):
        """Complete a pending promotion and return whether it was applied."""
        if not self.game_state.promotion_pending:
            return False
        self.promotion_executor.execute(chosen_type)
        return True

    def handle_undo_move(self):
        """Undo the latest move and return whether engine state changed."""
        if self.game_state.game_over:
            return False
        return self.undo_executor.execute()

    def _is_same_color_target(self, moved_piece, target_piece):
        """Return whether origin and target pieces have the same color."""
        target_color = piece_color(target_piece)
        return target_color is not None and piece_color(moved_piece) == target_color

