from chess_engine.helpers import EMP


class RecordLogger:
    def __init__(self, move_log, notation_converter):
        self.move_log = move_log
        self.notation_converter = notation_converter

    def record_move(
        self,
        moved_piece,
        moved_square,
        target_piece,
        target_square,
        move_type='MOVE'
    ):
        if move_type == 'MOVE' and target_piece != EMP:
            move_type = 'CAPTURE'

        from_notation = self.notation_converter.square_to_notation(moved_square)
        to_notation = self.notation_converter.square_to_notation(target_square)

        move_details = f"{moved_piece} {from_notation}->{to_notation}"

        if move_type == 'CAPTURE':
            move_details += f" x {target_piece}"
        elif move_type == 'EN_PASSANT':
            move_details += f" x {target_piece}"
        elif move_type == 'UNDO' and target_piece != EMP:
            move_details += f"; {target_piece} {from_notation}"
        elif move_type == 'PROMOTION':
            move_details += f"; {target_piece} {to_notation}"

        self._append_log(f"[{move_type}] {move_details}")

    def record_en_passant_undo(
        self,
        moved_piece,
        moved_square,
        target_square,
        captured_piece,
        captured_square
    ):
        from_notation = self.notation_converter.square_to_notation(moved_square)
        to_notation = self.notation_converter.square_to_notation(target_square)
        capture_notation = self.notation_converter.square_to_notation(captured_square)

        move_log = (
            f"[UNDO] {moved_piece} {from_notation}->{to_notation}; "
            f"{captured_piece} {capture_notation}"
        )

        self._append_log(move_log)

    def record_castling_move(self, moved_piece, moved_square, target_square, side):
        from_notation = self.notation_converter.square_to_notation(moved_square)
        to_notation = self.notation_converter.square_to_notation(target_square)

        castle_name = 'KINGSIDE' if side == 'king_side' else 'QUEENSIDE'
        move_log = (
            f"[CASTLING] {moved_piece} {from_notation}->{to_notation}; "
            f"{castle_name}"
        )

        self._append_log(move_log)

    def record_castling_undo(self, moved_piece, moved_square, target_square, side):
        from_notation = self.notation_converter.square_to_notation(moved_square)
        to_notation = self.notation_converter.square_to_notation(target_square)

        castle_name = 'KINGSIDE' if side == 'king_side' else 'QUEENSIDE'
        move_log = (
            f"[UNDO] {moved_piece} {from_notation}->{to_notation}; "
            f"{castle_name}"
        )

        self._append_log(move_log)

    def _append_log(self, move_log):
        self.move_log.append(move_log)
        print(move_log)