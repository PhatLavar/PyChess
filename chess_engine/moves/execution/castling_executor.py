from chess_engine.utilities import (
    EMP,
    CASTLING_ROOK_START,
    CASTLING_ROOK_TARGET,
    piece_color,
)
from chess_engine.moves.execution.state_updater import StateUpdater


class CastlingExecutor:
    """
    Apply and record a castling king-and-rook move.
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
        Move king and rook, remove rights, and record the completed turn.
        """
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

        self.state_updater.update_king_position(moved_piece, target_square)

        self.state_updater.remove_castling_rights_after_move(
            moved_piece,
            moved_square,
            EMP,
            target_square
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
        move_status, match_result = self.game_state.finish_turn()
        self.move_logger.record_castling_move(
            moved_piece,
            moved_square,
            target_square,
            side,
            move_type=move_status or 'CASTLING'
        )

        if match_result is not None:
            self.move_logger.record_end_match(match_result)
