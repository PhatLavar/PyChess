from chess_engine.moves.history.history_logger import HistoryLogger
from chess_engine.moves.history.notation_converter import NotationConverter
from chess_engine.moves.history.record_logger import RecordLogger


class MoveLogger:
    """
    Facade over human-readable records and structured undo history.
    """

    def __init__(self, board):
        """
        Create empty shared record and notation lists.
        """
        self.board = board
        self.move_log = []
        self.notation = []

        self.notation_converter = NotationConverter(board)
        self.record_logger = RecordLogger(
            self.move_log,
            self.notation_converter
        )
        self.history_logger = HistoryLogger(self.notation)

    def square_to_notation(self, square):
        """
        Return algebraic notation for a board square.
        """
        return self.notation_converter.square_to_notation(square)

    ####################################################################################
    # --------------------------------- NORMAL LOGS ------------------------------------
    ####################################################################################

    def record_move(
        self,
        moved_piece,
        moved_square,
        target_piece,
        target_square,
        move_type='MOVE'
    ):
        """
        Append a classified human-readable move entry.
        """
        self.record_logger.record_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square,
            move_type
        )

    def save_move(
        self,
        moved_piece,
        moved_square,
        target_piece,
        target_square,
        is_capture
    ):
        """
        Append structured ordinary-move history.
        """
        self.history_logger.save_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square,
            is_capture
        )

    ####################################################################################
    # ------------------------------- EN PASSANT LOGS ----------------------------------
    ####################################################################################

    def record_en_passant_undo(
        self,
        moved_piece,
        moved_square,
        target_square,
        captured_piece,
        captured_square
    ):
        """
        Append a human-readable en passant undo entry.
        """
        self.record_logger.record_en_passant_undo(
            moved_piece,
            moved_square,
            target_square,
            captured_piece,
            captured_square
        )

    def save_en_passant_move(
        self,
        moved_piece,
        moved_square,
        captured_piece,
        target_square,
        captured_square
    ):
        """
        Append structured en passant history.
        """
        self.history_logger.save_en_passant_move(
            moved_piece,
            moved_square,
            captured_piece,
            target_square,
            captured_square
        )

    ####################################################################################
    # -------------------------------- CASTLING LOGS -----------------------------------
    ####################################################################################

    def record_castling_move(
        self,
        moved_piece,
        moved_square,
        target_square,
        side,
        move_type='CASTLING'
    ):
        """
        Append a human-readable castling or checking entry.
        """
        self.record_logger.record_castling_move(
            moved_piece,
            moved_square,
            target_square,
            side,
            move_type
        )

    def record_castling_undo(
        self,
        moved_piece,
        moved_square,
        target_square,
        side
    ):
        """
        Append a human-readable castling undo entry.
        """
        self.record_logger.record_castling_undo(
            moved_piece,
            moved_square,
            target_square,
            side
        )

    def save_castling_move(
        self,
        moved_piece,
        moved_square,
        target_square,
        rook_piece,
        rook_square,
        rook_target_square,
        side
    ):
        """
        Append structured castling history.
        """
        self.history_logger.save_castling_move(
            moved_piece,
            moved_square,
            target_square,
            rook_piece,
            rook_square,
            rook_target_square,
            side
        )

    ####################################################################################
    # ------------------------------- PROMOTION LOGS -----------------------------------
    ####################################################################################

    def record_promotion_move(
        self,
        moved_piece,
        moved_square,
        target_piece,
        target_square,
        promotion_piece,
        move_type='PROMOTION'
    ):
        """
        Append a human-readable promotion or checking entry.
        """
        self.record_logger.record_promotion_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square,
            promotion_piece,
            move_type
        )

    def save_promotion_move(
        self,
        moved_piece,
        moved_square,
        target_piece,
        target_square,
        is_capture,
        promotion_piece
    ):
        """
        Append structured promotion history.
        """
        self.history_logger.save_promotion_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square,
            is_capture,
            promotion_piece
        )

    ####################################################################################
    # ------------------------------- ENDMATCH LOGS -----------------------------------
    ####################################################################################

    def record_end_match(self, result):
        """
        Append the final match result entry.
        """
        self.record_logger.record_end_match(result)
