from chess_engine.utilities import EMP


class HistoryLogger:
    """
    Append structured records required for reliable undo operations.
    """

    def __init__(self, notation):
        """
        Write into the supplied shared structured-history list.
        """
        self.notation = notation

    def save_move(
        self,
        moved_piece,
        moved_square,
        target_piece,
        target_square,
        is_capture
    ):
        """
        Save an ordinary move or capture record.
        """
        self.notation.append({
            'moved_piece': moved_piece,
            'moved_square': moved_square,
            'target_piece': target_piece,
            'target_square': target_square,
            'capture': is_capture,
        })

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
        Save a promotion record including the chosen piece.
        """
        self.notation.append({
            'moved_piece': moved_piece,
            'moved_square': moved_square,
            'target_piece': target_piece,
            'target_square': target_square,
            'capture': is_capture,
            'promotion_piece': promotion_piece,
        })

    def save_en_passant_move(
        self,
        moved_piece,
        moved_square,
        captured_piece,
        target_square,
        captured_square
    ):
        """
        Save en passant data including the removed pawn square.
        """
        self.notation.append({
            'moved_piece': moved_piece,
            'moved_square': moved_square,
            'target_piece': captured_piece,
            'target_square': target_square,
            'capture': True,
            'en_passant': True,
            'en_passant_capture_square': captured_square,
        })

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
        Save castling data for both the king and rook.
        """
        self.notation.append({
            'moved_piece': moved_piece,
            'moved_square': moved_square,
            'target_piece': EMP,
            'target_square': target_square,
            'capture': False,
            'castling': True,
            'castling_side': side,
            'rook_piece': rook_piece,
            'rook_square': rook_square,
            'rook_target_square': rook_target_square,
        })
