from chess_engine.moves.execution.state_updater import StateUpdater
from chess_engine.utilities import EMP


class EnPassantExecutor:
    """
    Apply and record en passant captures.
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


    def execute(self, moved_piece, moved_square, target_square):
        """
        Move the pawn, remove the adjacent pawn, and record the turn.
        """
        self.state_updater.save_castling_rights_state()

        captured_square = self.game_state.last_double_pawn_move['to_square']
        captured_piece = self.board.get_piece(captured_square)

        self.board.set_piece(target_square, moved_piece)
        self.board.set_piece(moved_square, EMP)
        self.board.set_piece(captured_square, EMP)

        self.move_logger.save_en_passant_move(
            moved_piece,
            moved_square,
            captured_piece,
            target_square,
            captured_square
        )

        self.state_updater.clear_en_passant_state()
        self.game_state.fifty_move_rule.record_move(
            moved_piece,
            is_capture=True,
        )
        move_status, match_result = self.game_state.finish_turn()
        self.move_logger.record_move(
            moved_piece,
            moved_square,
            captured_piece,
            target_square,
            move_type=move_status or 'EN_PASSANT'
        )

        if match_result is not None:
            self.move_logger.record_end_match(match_result)
