from chess_engine.moves.execution.state_updater import StateUpdater
from chess_engine.utilities import EMP


class NormalMoveExecutor:
    """
    Apply ordinary moves and captures.
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


    def execute(self, moved_piece, moved_square, target_piece, target_square):
        """
        Apply, classify, and record one ordinary move.
        """
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

    def _make_move(self, moved_piece, moved_square, target_square):
        """
        Move the piece and update a cached king position when necessary.
        """
        self.board.set_piece(target_square, moved_piece)
        self.board.set_piece(moved_square, EMP)
        self.state_updater.update_king_position(moved_piece, target_square)

    def _record_successful_move(
        self,
        moved_piece,
        moved_square,
        target_piece,
        target_square,
        move_type
    ):
        """
        Write the human log entry and structured undo history.
        """
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
