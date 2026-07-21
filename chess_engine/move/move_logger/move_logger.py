from chess_engine.move.move_logger.notation_converter import NotationConverter
from chess_engine.move.move_logger.record_logger import RecordLogger
from chess_engine.move.move_logger.history_logger import HistoryLogger


class MoveLogger:
    def __init__(self, board):
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
        return self.notation_converter.square_to_notation(square)

    def record_move(
        self,
        moved_piece,
        moved_square,
        target_piece,
        target_square,
        move_type='MOVE'
    ):
        self.record_logger.record_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square,
            move_type
        )

    def record_en_passant_undo(
        self,
        moved_piece,
        moved_square,
        target_square,
        captured_piece,
        captured_square
    ):
        self.record_logger.record_en_passant_undo(
            moved_piece,
            moved_square,
            target_square,
            captured_piece,
            captured_square
        )

    def record_castling_move(self, moved_piece, moved_square, target_square, side):
        self.record_logger.record_castling_move(
            moved_piece,
            moved_square,
            target_square,
            side
        )

    def record_castling_undo(self, moved_piece, moved_square, target_square, side):
        self.record_logger.record_castling_undo(
            moved_piece,
            moved_square,
            target_square,
            side
        )

    def save_move(
        self,
        moved_piece,
        moved_square,
        target_piece,
        target_square,
        is_capture
    ):
        self.history_logger.save_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square,
            is_capture
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
        self.history_logger.save_promotion_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square,
            is_capture,
            promotion_piece
        )

    def save_en_passant_move(
        self,
        moved_piece,
        moved_square,
        captured_piece,
        target_square,
        captured_square
    ):
        self.history_logger.save_en_passant_move(
            moved_piece,
            moved_square,
            captured_piece,
            target_square,
            captured_square
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
        self.history_logger.save_castling_move(
            moved_piece,
            moved_square,
            target_square,
            rook_piece,
            rook_square,
            rook_target_square,
            side
        )