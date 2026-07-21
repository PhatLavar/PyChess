from chess_engine.helpers import EMP, piece_color
from chess_engine.move.move_executor.state_updater import StateUpdater


class PawnPromotionExecutor:
    def __init__(self, game_state, move_logger):
        self.game_state = game_state
        self.move_logger = move_logger
        self.state_updater = StateUpdater(game_state)


    @property
    def board(self):
        return self.game_state.board


    def set_pending_state(self, moved_piece, moved_square, target_piece, target_square):
        self.game_state.promotion_pending = True
        self.game_state.promotion_square = target_square
        self.game_state.promotion_moved_square = moved_square
        self.game_state.promotion_moved_piece = moved_piece
        self.game_state.promotion_target_piece = target_piece
        self.game_state.promotion_color = piece_color(moved_piece)


    def execute(self, chosen_type):
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

        self.move_logger.record_move(
            moved_piece,
            moved_square,
            promoted_piece,
            target_square,
            move_type='PROMOTION'
        )

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
        self._record_game_status(promoted_piece, moved_square, target_piece, target_square)
        self.state_updater.reset_click_state()


    def _clear_promotion_state(self):
        self.game_state.promotion_pending = False
        self.game_state.promotion_square = None
        self.game_state.promotion_moved_square = None
        self.game_state.promotion_moved_piece = None
        self.game_state.promotion_target_piece = None
        self.game_state.promotion_color = None


    def _record_game_status(self, moved_piece, moved_square, target_piece, target_square):
        self.game_state.white_to_move = not self.game_state.white_to_move
        validator = self.game_state.move_validator

        if validator.is_checkmate():
            self.move_logger.record_move(
                moved_piece,
                moved_square,
                target_piece,
                target_square,
                move_type='CHECKMATE'
            )

        elif validator.is_stalemate():
            self.move_logger.record_move(
                moved_piece,
                moved_square,
                target_piece,
                target_square,
                move_type='STALEMATE'
            )
            
        elif validator._in_check():
            self.move_logger.record_move(
                moved_piece,
                moved_square,
                target_piece,
                target_square,
                move_type='CHECK'
            )