class MoveLogger:
    def __init__(self, board):
        self.board = board
        self.move_log = []
        self.notation = []


    ####################################################################################
    # -------------------------------- LOG MOVE RECORD ---------------------------------
    ####################################################################################
    def square_to_notation(self, square):
        files = 'abcdefgh'
        row, col = square
        file = files[col]
        rank = str(self.board.DIMENSION - row)
        return f"{file}{rank}"
    
    def record_move(self, moved_piece, moved_square, target_piece, target_square, move_type='MOVE'):
        if move_type == 'MOVE' and target_piece != '--':
            move_type = 'CAPTURE'

        from_notation = self.square_to_notation(moved_square)
        to_notation = self.square_to_notation(target_square)

        move_details = f"{moved_piece} {from_notation}->{to_notation}"
        if move_type == 'CAPTURE':
            move_details += f" x {target_piece}"
        elif move_type == 'EN_PASSANT':
            move_details += f" x {target_piece}"
        elif move_type == 'UNDO' and target_piece != '--':
            move_details += f"; {target_piece} {from_notation}"
        elif move_type == 'PROMOTION':
            move_details += f"; {target_piece} {to_notation}"

        move_log = f"[{move_type}] {move_details}"
        self.move_log.append(move_log)
        print(move_log)

    def record_en_passant_undo(self, moved_piece, moved_square, target_square, captured_piece, captured_square):
        from_notation = self.square_to_notation(moved_square)
        to_notation = self.square_to_notation(target_square)
        capture_notation = self.square_to_notation(captured_square)

        move_log = f"[UNDO] {moved_piece} {from_notation}->{to_notation}; {captured_piece} {capture_notation}"
        self.move_log.append(move_log)
        print(move_log)

    
    ####################################################################################
    # ------------------------------ SAVE MOVE NOTATION --------------------------------
    ####################################################################################
    def save_move(self, moved_piece, moved_square, target_piece, target_square, is_capture):
        self.notation.append({
            'moved_piece': moved_piece,
            'moved_square': moved_square,
            'target_piece': target_piece,
            'target_square': target_square,
            'capture': is_capture,
        })

    def save_promotion_move(self, moved_piece, moved_square, target_piece, target_square, is_capture, promotion_piece):
        self.notation.append({
            'moved_piece': moved_piece,
            'moved_square': moved_square,
            'target_piece': target_piece,
            'target_square': target_square,
            'capture': is_capture,
            'promotion_piece': promotion_piece,
        })

    def save_en_passant_move(self, moved_piece, moved_square, captured_piece, target_square, captured_square):
        self.notation.append({
            'moved_piece': moved_piece,
            'moved_square': moved_square,
            'target_piece': captured_piece,
            'target_square': target_square,
            'capture': True,
            'en_passant': True,
            'en_passant_capture_square': captured_square,
        })
