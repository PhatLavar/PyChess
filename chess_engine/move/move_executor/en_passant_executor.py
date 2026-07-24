from chess_engine.helpers import EMP
from chess_engine.move.move_executor.state_updater import StateUpdater


class EnPassantExecutor:
    def __init__(self, game_state, move_logger):
        self.game_state = game_state
        self.move_logger = move_logger
        self.state_updater = StateUpdater(game_state)


    @property
    def board(self):
        return self.game_state.board


    def execute(self, moved_piece, moved_square, target_square):
        self.state_updater.save_castling_rights_state()

        captured_square = self.game_state.last_double_pawn_move['to_square']
        captured_piece = self.board.get_piece(captured_square)

        self.board.set_piece(target_square, moved_piece)
        self.board.set_piece(moved_square, EMP)
        self.board.set_piece(captured_square, EMP)

        self.game_state.move_animation.start(
            moved_piece,
            moved_square,
            target_square
        )

        self.move_logger.record_move(
            moved_piece,
            moved_square,
            captured_piece,
            target_square,
            move_type='EN_PASSANT'
        )

        self.move_logger.save_en_passant_move(
            moved_piece,
            moved_square,
            captured_piece,
            target_square,
            captured_square
        )

        self.state_updater.clear_en_passant_state()
        self._record_game_status(moved_piece, moved_square, captured_piece, target_square)
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