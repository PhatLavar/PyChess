from chess_engine.helpers import EMP
from chess_engine.move.move_executor.state_updater import StateUpdater


class NormalMoveExecutor:
    def __init__(self, game_state, move_logger):
        self.game_state = game_state
        self.move_logger = move_logger
        self.state_updater = StateUpdater(game_state)


    @property
    def board(self):
        return self.game_state.board


    def execute(self, moved_piece, moved_square, target_piece, target_square):
        self.state_updater.save_castling_rights_state()
        self.state_updater.remove_castling_rights_after_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square
        )

        self._make_move(moved_piece, moved_square, target_square)
        self.state_updater.update_en_passant_state(
            moved_piece,
            moved_square,
            target_square
        )

        move_status, match_result = self.game_state.finish_turn()
        self._record_successful_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square,
            move_status or 'MOVE'
        )

        if match_result is not None:
            self.move_logger.record_end_match(match_result)

        self.state_updater.reset_click_state()


    def _make_move(self, moved_piece, moved_square, target_square):
        self.board.set_piece(target_square, moved_piece)
        self.board.set_piece(moved_square, EMP)
        self.state_updater.update_king_position(moved_piece, target_square)

        self.game_state.move_animation.start(
            moved_piece,
            moved_square,
            target_square
        )


    def _record_successful_move(
        self,
        moved_piece,
        moved_square,
        target_piece,
        target_square,
        move_type
    ):
        is_capture = target_piece != EMP

        self.move_logger.record_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square,
            move_type=move_type
        )

        self.move_logger.save_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square,
            is_capture
        )
