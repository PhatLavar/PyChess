from chess_engine.utilities import EMP


class RecordLogger:
    """
    Build and print human-readable move-log entries.
    """

    def __init__(self, move_log, notation_converter):
        """
        Write into the supplied log using the shared square converter.
        """
        self.move_log = move_log
        self.notation_converter = notation_converter

    ####################################################################################
    # ------------------------------- NORMAL MOVE LOG ----------------------------------
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
        Append one classified ordinary, capture, check, or undo entry.
        """
        if move_type == 'MOVE' and target_piece != EMP:
            move_type = 'CAPTURE'

        from_notation = self.notation_converter.square_to_notation(moved_square)
        to_notation = self.notation_converter.square_to_notation(target_square)

        move_details = f"{moved_piece} {from_notation}->{to_notation}"

        if target_piece != EMP and move_type in (
            'CAPTURE', 'EN_PASSANT', 'CHECK', 'CHECKMATE', 'STALEMATE'
        ):
            move_details += f" x {target_piece}"
        elif move_type == 'UNDO' and target_piece != EMP:
            move_details += f"; {target_piece} {from_notation}"
        elif move_type == 'PROMOTION':
            move_details += f"; {target_piece} {to_notation}"

        self._append_log(f"[{move_type}] {move_details}")

    ####################################################################################
    # ----------------------------- PROMOTION MOVE LOG ---------------------------------
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
        """Append one promotion entry while preserving capture details."""
        from_notation = self.notation_converter.square_to_notation(moved_square)
        to_notation = self.notation_converter.square_to_notation(target_square)
        move_details = f"{moved_piece} {from_notation}->{to_notation}"

        if target_piece != EMP:
            move_details += f" x {target_piece}"

        move_details += f"; {promotion_piece} {to_notation}"
        self._append_log(f"[{move_type}] {move_details}")

    ####################################################################################
    # ---------------------------- EN PASSANT MOVE LOG ---------------------------------
    ####################################################################################

    def record_en_passant_undo(
        self,
        moved_piece,
        moved_square,
        target_square,
        captured_piece,
        captured_square
    ):
        """Append an undo entry that identifies the restored pawn square."""
        from_notation = self.notation_converter.square_to_notation(moved_square)
        to_notation = self.notation_converter.square_to_notation(target_square)
        capture_notation = self.notation_converter.square_to_notation(captured_square)

        move_log = (
            f"[UNDO] {moved_piece} {from_notation}->{to_notation}; "
            f"{captured_piece} {capture_notation}"
        )

        self._append_log(move_log)

    ####################################################################################
    # ----------------------------- CASTLING MOVE LOG ----------------------------------
    ####################################################################################

    def record_castling_move(
        self,
        moved_piece,
        moved_square,
        target_square,
        side,
        move_type='CASTLING'
    ):
        """Append a castling entry, or its higher-priority check status."""
        from_notation = self.notation_converter.square_to_notation(moved_square)
        to_notation = self.notation_converter.square_to_notation(target_square)

        castle_name = 'KINGSIDE' if side == 'king_side' else 'QUEENSIDE'
        move_log = (
            f"[{move_type}] {moved_piece} {from_notation}->{to_notation}; "
            f"{castle_name}"
        )

        self._append_log(move_log)

    def record_castling_undo(self, moved_piece, moved_square, target_square, side):
        """Append an undo entry for a castling move."""
        from_notation = self.notation_converter.square_to_notation(moved_square)
        to_notation = self.notation_converter.square_to_notation(target_square)

        castle_name = 'KINGSIDE' if side == 'king_side' else 'QUEENSIDE'
        move_log = (
            f"[UNDO] {moved_piece} {from_notation}->{to_notation}; "
            f"{castle_name}"
        )

        self._append_log(move_log)

    ####################################################################################
    # ----------------------------- ENDMATCH MOVE LOG ----------------------------------
    ####################################################################################

    def record_end_match(self, result):
        """Append the final ``ENDMATCH`` result entry."""
        display_result = result
        self._append_log(f"[ENDMATCH] {display_result}")

    ####################################################################################
    # ------------------------------ MOVE LOG HELPERS ----------------------------------
    ####################################################################################

    def _append_log(self, move_log):
        """Store and print one completed log string."""
        self.move_log.append(move_log)
        print(move_log)
