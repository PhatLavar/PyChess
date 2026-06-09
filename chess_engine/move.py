class Move:
    def __init__(self, game_state):
        self.game_state = game_state
        self.move_log = []          # ["wP e2->e4", "wP e2->e4 x bP"]
        self.notation = []          # {'moved_piece', 'moved_square', 'target_piece', 'target_square', 'capture'}



    ####################################################################################
    # ------------------------------- HANDLE PIECE MOVE --------------------------------
    ####################################################################################
    def handle_selected_piece_move(self, moved_square, target_square):
        if self.game_state.moved_piece == '--':
            self.game_state.selected_square = ()
            self.game_state.player_clicked = []
            return

        def color_of(piece):
            # 'w' or 'b'
            return None if piece == '--' else piece[0]

        moved_color = color_of(self.game_state.moved_piece)
        target_color = color_of(self.game_state.target_piece)

        # rule: same color -> no harm, not working for 'castling' yet
        if target_color is not None and moved_color == target_color:
            self.game_state.player_clicked = []
            self.game_state.selected_square = ()
            self.game_state.player_clicked.append(target_square)
            return

        capture = self.game_state.target_piece != '--'
        self.game_state.board.board[target_square[0]][target_square[1]] = self.game_state.moved_piece
        self.game_state.board.board[moved_square[0]][moved_square[1]] = '--'

        # record the move and save undo metadata
        self.record_move(self.game_state.moved_piece, moved_square, self.game_state.target_piece, target_square, capture)
        self.notation.append({
            'moved_piece': self.game_state.moved_piece,
            'moved_square': moved_square,
            'target_piece': self.game_state.target_piece,
            'target_square': target_square,
            'capture': capture,
        })

        # reset
        self.game_state.selected_square = ()
        self.game_state.player_clicked = []
        self.game_state.white_to_move = not self.game_state.white_to_move



    ####################################################################################
    # -------------------------------- RECORD MOVE LOG ---------------------------------
    ####################################################################################
    def record_move(self, moved_piece, moved_square, target_piece, target_square, capture, redo = False):
        """
        Format, store and print a simple move notation.
        Example: 'wP e2->e4' or 'wP e2->e4 x bP' when capturing.
        """
        def square_to_notation(square):
            files = 'abcdefgh'
            row, col = square
            file = files[col]
            rank = str(self.game_state.board.DIMENSION - row)
            return f"{file}{rank}"

        from_notation = square_to_notation(moved_square)
        to_notation = square_to_notation(target_square)

        if redo:
            move_log = f"[REDO] {moved_piece} {from_notation}->{to_notation}"
        else:
            move_log = f"{moved_piece} {from_notation}->{to_notation}"

        if capture:
            move_log += f" x {target_piece}"
        
        self.move_log.append(move_log)
        print(move_log)



    ####################################################################################
    # ------------------------------- HANDLE UNDO MOVE ---------------------------------
    ####################################################################################
    def handle_undo_move(self):
        if len(self.notation) == 0:
            return

        last_move = self.notation.pop()
        moved_square = last_move['moved_square']
        target_square = last_move['target_square']
        moved_piece = last_move['moved_piece']
        target_prev_piece = last_move['target_piece']

        self.game_state.board.board[moved_square[0]][moved_square[1]] = moved_piece
        self.game_state.board.board[target_square[0]][target_square[1]] = target_prev_piece

        if len(self.move_log) > 0:
            self.move_log.pop()

        self.record_move(moved_piece, target_square, target_prev_piece, moved_square, last_move['capture'], True)

        self.game_state.selected_square = ()
        self.game_state.player_clicked = []
        self.game_state.white_to_move = not self.game_state.white_to_move
    

    def get_all_possible_moves(self, chess_piece):
        pass


    def get_all_valid_moves(self, chess_piece):
        self.get_all_possible_moves # we won't consider the check after moving! (yet)

    
    ####################################################################################
    # --------------------------------- PIECES MOVE ------------------------------------
    ####################################################################################
    def get_pawn_move(self):
        pass


    def get_rook_move(self):
        pass


    def get_bishop_move(self):
        pass


    def get_knight_move(self):
        pass


    def get_king_move(self):
        pass


    def get_queen_move(self):
        pass







