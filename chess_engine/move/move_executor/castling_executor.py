from chess_engine.helpers import (
    EMP,
    CASTLING_ROOK_START,
    CASTLING_ROOK_TARGET,
    piece_color,
)
from chess_engine.move.move_executor.state_updater import StateUpdater


class CastlingExecutor:
    def __init__(self, game_state, move_logger):
        self.game_state = game_state
        self.move_logger = move_logger
        self.state_updater = StateUpdater(game_state)


    @property
    def board(self):
        return self.game_state.board


    def execute(self, moved_piece, moved_square, target_square):
        color = piece_color(moved_piece)
        side = 'king_side' if target_square[1] > moved_square[1] else 'queen_side'

        rook_start = CASTLING_ROOK_START[color][side]
        rook_target = CASTLING_ROOK_TARGET[color][side]
        rook_piece = self.board.get_piece(rook_start)

        self.state_updater.save_castling_rights_state()

        self.board.set_piece(target_square, moved_piece)
        self.board.set_piece(moved_square, EMP)

        self.board.set_piece(rook_target, rook_piece)
        self.board.set_piece(rook_start, EMP)

        self.game_state.move_animation.start(
            moved_piece,
            moved_square,
            target_square
        )
        self.game_state.move_animation.start(
            rook_piece,
            rook_start,
            rook_target
        )

        self.state_updater.update_king_position(moved_piece, target_square)

        self.state_updater.remove_castling_rights_after_move(
            moved_piece,
            moved_square,
            EMP,
            target_square
        )

        self.move_logger.record_castling_move(
            moved_piece,
            moved_square,
            target_square,
            side
        )

        self.move_logger.save_castling_move(
            moved_piece,
            moved_square,
            target_square,
            rook_piece,
            rook_start,
            rook_target,
            side
        )

        self.state_updater.clear_en_passant_state()
        self._record_game_status(moved_piece, moved_square, EMP, target_square)
        self.state_updater.reset_click_state()


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