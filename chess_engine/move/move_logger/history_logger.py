from chess_engine.helpers import EMP


class HistoryLogger:
    def __init__(self, notation):
        self.notation = notation

    def save_move(
        self,
        moved_piece,
        moved_square,
        target_piece,
        target_square,
        is_capture
    ):
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