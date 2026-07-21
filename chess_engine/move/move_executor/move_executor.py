from chess_engine.helpers import EMP
from chess_engine.move.move_executor.normal_executor import NormalMoveExecutor
from chess_engine.move.move_executor.pawn_promotion_executor import PawnPromotionExecutor
from chess_engine.move.move_executor.en_passant_executor import EnPassantExecutor
from chess_engine.move.move_executor.castling_executor import CastlingExecutor
from chess_engine.move.move_executor.undo_executor import UndoExecutor


class MoveExecutor:
    def __init__(self, game_state, move_generator, move_logger):
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
        return self.game_state.board

    def handle_piece_move(self, moved_square, target_square):
        moved_piece = self.game_state.moved_piece
        target_piece = self.game_state.target_piece

        if moved_piece == EMP:
            self._reset_click_state()
            return

        if self._is_same_color_target(moved_piece, target_piece):
            self._reset_click_state()
            self.game_state.player_clicked.append(target_square)
            return

        if (moved_square, target_square) not in self.move_generator.get_valid_moves():
            self.move_logger.record_move(
                moved_piece,
                moved_square,
                target_piece,
                target_square,
                move_type='INVALID'
            )
            self._reset_click_state()
            return

        validator = self.game_state.move_validator

        if validator.is_en_passant_move(moved_piece, moved_square, target_square):
            self.en_passant_executor.execute(moved_piece, moved_square, target_square)
            return

        if moved_piece[1] == 'P' and validator.can_pawn_promotion(target_square):
            self.promotion_executor.set_pending_state(
                moved_piece,
                moved_square,
                target_piece,
                target_square
            )
            return

        if validator.is_castling_move(moved_piece, moved_square, target_square):
            self.castling_executor.execute(moved_piece, moved_square, target_square)
            return

        self.normal_executor.execute(
            moved_piece,
            moved_square,
            target_piece,
            target_square
        )

    def handle_pawn_promotion(self, chosen_type):
        self.promotion_executor.execute(chosen_type)

    def handle_undo_move(self):
        self.undo_executor.execute()

    def _is_same_color_target(self, moved_piece, target_piece):
        from chess_engine.helpers import piece_color
        target_color = piece_color(target_piece)
        return target_color is not None and piece_color(moved_piece) == target_color

    def _reset_click_state(self):
        self.game_state.selected_square = ()
        self.game_state.player_clicked = []