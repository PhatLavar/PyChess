from chess_engine.helper import EMP, piece_color

class MoveExecutor:
    def __init__(self, game_state, move_generator, move_logger):
        self.game_state = game_state
        self.move_generator = move_generator
        self.move_logger = move_logger

    @property
    def board(self):
        return self.game_state.board


    ####################################################################################
    # ------------------------------- HANDLE PIECE MOVE --------------------------------
    ####################################################################################
    def handle_piece_move(self, moved_square, target_square):
        moved_piece = self.game_state.moved_piece
        target_piece = self.game_state.target_piece
        can_promote_pawn = self.game_state.move_validator.can_pawn_promotion(target_square)
        is_en_passant_move = self.game_state.move_validator.is_en_passant_move(moved_piece, moved_square, target_square)

        if moved_piece == EMP:
            self._reset_click_state()
            return

        if self._is_same_color_target(moved_piece, target_piece):
            self._reset_click_state()
            self.game_state.player_clicked.append(target_square)
            return

        if (moved_square, target_square) not in self.move_generator.get_valid_moves():
            self.move_logger.record_move(moved_piece, moved_square, target_piece, target_square, move_type='INVALID')
            self._reset_click_state()
            return

        if is_en_passant_move:
            self.handle_en_passant(moved_piece, moved_square, target_square)
            return
        
        if moved_piece[1] == 'P' and can_promote_pawn:
            self.handle_promotion_state(moved_piece, moved_square, target_piece, target_square)
            return

        self._make_move(moved_piece, moved_square, target_square)
        self._record_successful_move(moved_piece, moved_square, target_piece, target_square)
        self._update_en_passant_state(moved_piece, moved_square, target_square)
        self._record_game_status(moved_piece, moved_square, target_piece, target_square)
        self._reset_click_state()


    ####################################################################################
    # ------------------------------- HANDLE UNDO MOVE ---------------------------------
    ####################################################################################
    def handle_undo_move(self):
        if self.game_state.promotion_pending:
            self._clear_promotion_state()
            self._reset_click_state()
            return

        if len(self.move_logger.notation) == 0:
            return

        last_move = self.move_logger.notation.pop()
        moved_square = last_move['moved_square']
        target_square = last_move['target_square']
        moved_piece = last_move['moved_piece']
        target_prev_piece = last_move['target_piece']

        if last_move.get('en_passant'):
            self.board.set_piece(moved_square, moved_piece)
            self.board.set_piece(target_square, EMP)
            self.board.set_piece(last_move['en_passant_capture_square'], target_prev_piece)
        else:
            self.board.set_piece(moved_square, moved_piece)
            self.board.set_piece(target_square, target_prev_piece)

        self._restore_en_passant_state_after_undo(last_move)
        self._update_king_position(moved_piece, moved_square)

        if len(self.move_logger.move_log) > 0:
            self.move_logger.move_log.pop()

        if last_move.get('en_passant'):
            self.move_logger.record_en_passant_undo(
                moved_piece,
                target_square,
                moved_square,
                target_prev_piece,
                last_move['en_passant_capture_square']
            )
        else:
            self.move_logger.record_move(moved_piece, target_square, target_prev_piece, moved_square, move_type='REDO')
        self._reset_click_state()
        self.game_state.white_to_move = not self.game_state.white_to_move


    ####################################################################################
    # ----------------------------- HANDLE MOVE HELPERS --------------------------------
    ####################################################################################
    def _is_same_color_target(self, moved_piece, target_piece):
        target_color = piece_color(target_piece)
        return target_color is not None and piece_color(moved_piece) == target_color

    def _make_move(self, moved_piece, moved_square, target_square):
        self.board.set_piece(target_square, moved_piece)
        self.board.set_piece(moved_square, EMP)
        self._update_king_position(moved_piece, target_square)

    def _record_successful_move(self, moved_piece, moved_square, target_piece, target_square):
        is_capture = target_piece != EMP
        self.move_logger.record_move(moved_piece, moved_square, target_piece, target_square, move_type='MOVE')
        self.move_logger.save_move(moved_piece, moved_square, target_piece, target_square, is_capture)

    def _record_game_status(self, moved_piece, moved_square, target_piece, target_square):
        self.game_state.white_to_move = not self.game_state.white_to_move
        validator = self.game_state.move_validator

        if validator.is_checkmate():
            self.move_logger.record_move(moved_piece, moved_square, target_piece, target_square, move_type='CHECKMATE')
        elif validator.is_stalemate():
            self.move_logger.record_move(moved_piece, moved_square, target_piece, target_square, move_type='STALEMATE')
        elif validator._in_check():
            self.move_logger.record_move(moved_piece, moved_square, target_piece, target_square, move_type='CHECK')

    def _update_king_position(self, piece, square):
        if piece == 'wK':
            self.game_state.white_king_position = square
        elif piece == 'bK':
            self.game_state.black_king_position = square

    def _restore_en_passant_state_after_undo(self, undone_move):
        self._clear_en_passant_state()

        if len(self.move_logger.notation) == 0:
            return

        previous_move = self.move_logger.notation[-1]
        moved_piece = previous_move['moved_piece']
        moved_square = previous_move['moved_square']
        target_square = previous_move['target_square']

        if moved_piece[1] != 'P':
            return

        if abs(target_square[0] - moved_square[0]) != 2:
            return

        self.game_state.last_double_pawn_move = {
            'pawn': moved_piece,
            'from_square': moved_square,
            'to_square': target_square,
        }
        self.game_state.en_passant_target = (
            (moved_square[0] + target_square[0]) // 2,
            moved_square[1]
        )

    def _reset_click_state(self):
        self.game_state.selected_square = ()
        self.game_state.player_clicked = []


    ####################################################################################
    # ---------------------------- HANDLE PAWN PROMOTION -------------------------------
    ####################################################################################
    def handle_pawn_promotion(self, chosen_type):
        moved_piece = self.game_state.promotion_moved_piece
        moved_square = self.game_state.promotion_moved_square
        target_piece = self.game_state.promotion_target_piece
        target_square = self.game_state.promotion_square
        promoted_piece = self.game_state.promotion_color + chosen_type
        is_capture = target_piece != EMP

        self.board.set_piece(target_square, promoted_piece)
        self.board.set_piece(moved_square, EMP)
        
        self.move_logger.record_move(
            moved_piece,
            moved_square,
            promoted_piece,
            target_square,
            move_type='PROMOTION'
        )
        self.move_logger.save_promotion_move(
            moved_piece,
            moved_square,
            target_piece,
            target_square,
            is_capture,
            promotion_piece=promoted_piece
        )

        self._clear_promotion_state()
        self._clear_en_passant_state()
        self._record_game_status(promoted_piece, moved_square, target_piece, target_square)
        self._reset_click_state()
    
    def handle_promotion_state(self, moved_piece, moved_square, target_piece, target_square):
        self.game_state.promotion_pending = True
        self.game_state.promotion_square = target_square
        self.game_state.promotion_moved_square = moved_square
        self.game_state.promotion_moved_piece = moved_piece
        self.game_state.promotion_target_piece = target_piece
        self.game_state.promotion_color = piece_color(moved_piece)

    def _clear_promotion_state(self):
        self.game_state.promotion_pending = False
        self.game_state.promotion_square = None
        self.game_state.promotion_moved_square = None
        self.game_state.promotion_moved_piece = None
        self.game_state.promotion_target_piece = None
        self.game_state.promotion_color = None


    ####################################################################################
    # ------------------------------ HANDLE EN PASSANT ---------------------------------
    ####################################################################################
    def handle_en_passant(self, moved_piece, moved_square, target_square):
        captured_square = self.game_state.last_double_pawn_move['to_square']
        captured_piece = self.board.get_piece(captured_square)

        self.board.set_piece(target_square, moved_piece)
        self.board.set_piece(moved_square, EMP)
        self.board.set_piece(captured_square, EMP)

        self.move_logger.record_move(
            moved_piece,
            moved_square,
            captured_piece,
            target_square,
            move_type='EN_PASSANT'
        )
        self.move_logger.save_en_passant_move(
            moved_piece,
            moved_square,
            captured_piece,
            target_square,
            captured_square
        )

        self._clear_en_passant_state()
        self._record_game_status(moved_piece, moved_square, captured_piece, target_square)
        self._reset_click_state()

    def _clear_en_passant_state(self):
        self.game_state.last_double_pawn_move = None
        self.game_state.en_passant_target = None

    def _update_en_passant_state(self, moved_piece, moved_square, target_square):
        self._clear_en_passant_state()
        is_pawn = moved_piece[1] == 'P'
        moved_two_rows = abs(target_square[0] - moved_square[0]) == 2

        if not is_pawn or not moved_two_rows:
            return

        self.game_state.last_double_pawn_move = {
            'pawn': moved_piece,
            'from_square': moved_square,
            'to_square': target_square,
        }

        self.game_state.en_passant_target = (
            (moved_square[0] + target_square[0]) // 2,
            moved_square[1]
        )
