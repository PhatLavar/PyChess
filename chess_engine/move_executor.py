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

        self._make_move(moved_piece, moved_square, target_square)
        self._record_successful_move(moved_piece, moved_square, target_piece, target_square)
        self._record_game_status(moved_piece, moved_square, target_piece, target_square)
        self._reset_click_state()


    ####################################################################################
    # ------------------------------- HANDLE UNDO MOVE ---------------------------------
    ####################################################################################
    def handle_undo_move(self):
        if len(self.move_logger.notation) == 0:
            return

        last_move = self.move_logger.notation.pop()
        moved_square = last_move['moved_square']
        target_square = last_move['target_square']
        moved_piece = last_move['moved_piece']
        target_prev_piece = last_move['target_piece']

        self.board.set_piece(moved_square, moved_piece)
        self.board.set_piece(target_square, target_prev_piece)
        self._update_king_position(moved_piece, moved_square)

        if len(self.move_logger.move_log) > 0:
            self.move_logger.move_log.pop()

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

    def _reset_click_state(self):
        self.game_state.selected_square = ()
        self.game_state.player_clicked = []
