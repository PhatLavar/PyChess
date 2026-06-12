class Move:
    def __init__(self, game_state):
        self.game_state = game_state
        self.move_log = []          # ["wP e2->e4", "wP e2->e4 x bP"]
        self.notation = []          # {'moved_piece', 'moved_square', 'target_piece', 'target_square', 'capture'}
        self.get_move_functions = {
            'P': self.get_pawn_move,
            'R': self.get_rook_move,
            'B': self.get_bishop_move,
            'Q': self.get_queen_move,
            'K': self.get_king_move,
            'N': self.get_knight_move,
        }



    ####################################################################################
    # ------------------------------- HANDLE PIECE MOVE --------------------------------
    ####################################################################################
    def _color_of_pieces(self, moved_piece, target_piece):
        moved_piece_color = None if moved_piece == '--' else moved_piece[0]
        target_piece_color = None if target_piece == '--' else target_piece[0]
        return (moved_piece_color, target_piece_color)
    

    def _reset_click_state(self):
        self.game_state.selected_square = ()
        self.game_state.player_clicked = []

    
    def handle_piece_move(self, moved_square, target_square):
        # Initially setup the variable
        moved_piece = self.game_state.moved_piece
        target_piece = self.game_state.target_piece

        if moved_piece == '--':
            self._reset_click_state()
            return
        
        valid_moves = self.get_valid_moves()
        current_move = (moved_square, target_square)
        moved_piece_color, target_piece_color = self._color_of_pieces(moved_piece, target_piece)

        # Rule: same color -> no harm, not working for 'castling' yet
        if target_piece_color is not None and moved_piece_color == target_piece_color:
            self._reset_click_state()
            self.game_state.player_clicked.append(target_square)
            return
        
        # Rule: if the move is INVALID, no making it and reset the clicking state buffer
        if current_move not in valid_moves:
            self.record_move(moved_piece, moved_square, target_piece, target_square, move_type='INVALID')
            self._reset_click_state()
            return

        # Stimulate the move
        is_capture = self.game_state.target_piece != '--'
        self.game_state.board.board[target_square[0]][target_square[1]] = self.game_state.moved_piece
        self.game_state.board.board[moved_square[0]][moved_square[1]] = '--'

        # Update the king location if it is a king move
        if moved_piece == 'wK':
            self.game_state.white_king_position = target_square
        elif moved_piece == 'bK':
            self.game_state.black_king_position = target_square

        # Record the move and save undo metadata
        self.record_move(moved_piece, moved_square, target_piece, target_square, move_type='MOVE')
        self.notation.append({
            'moved_piece': moved_piece,
            'moved_square': moved_square,
            'target_piece': target_piece,
            'target_square': target_square,
            'capture': is_capture,
        })

        # Reset
        self._reset_click_state()
        self.game_state.white_to_move = not self.game_state.white_to_move



    ####################################################################################
    # -------------------------------- RECORD MOVE LOG ---------------------------------
    ####################################################################################
    def _square_to_notation(self, square):
            files = 'abcdefgh'
            row, col = square
            file = files[col]
            rank = str(self.game_state.board.DIMENSION - row)
            return f"{file}{rank}"
    

    def record_move(self, moved_piece, moved_square, target_piece, target_square, move_type='MOVE'):
        """
        Format, store and print a simple move notation.
        Example: 'wP e2->e4' or 'wP e2->e4 x bP' when capturing.

        Accepted move_types: 'MOVE', 'CAPTURE', 'REDO', 'INVALID'
        """
        if move_type == 'MOVE' and target_piece != '--':
            move_type = 'CAPTURE'

        from_notation = self._square_to_notation(moved_square)
        to_notation = self._square_to_notation(target_square)

        move_details = f"{moved_piece} {from_notation}->{to_notation}"
        if move_type == 'CAPTURE':
            move_details += f" x {target_piece}"
        elif move_type == 'REDO':
            if target_piece != '--':
                move_details += f"; {target_piece} {from_notation}"

        # Combine flag and details
        move_log = f"[{move_type}] {move_details}"
        
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

        # Update the king location when redo a king move
        if moved_piece == 'wK':
            self.game_state.white_king_location = moved_square
        elif moved_piece == 'bK':
            self.game_state.black_king_location = moved_square

        if len(self.move_log) > 0:
            self.move_log.pop()

        self.record_move(moved_piece, target_square, target_prev_piece, moved_square, move_type='REDO')

        self._reset_click_state()
        self.game_state.white_to_move = not self.game_state.white_to_move



    ####################################################################################
    # ----------------------------- GET ALL VALID MOVES --------------------------------
    ####################################################################################
    def get_valid_moves(self):
        possible_moves = self.get_all_possible_moves()
        valid_moves = [] # [((moved_row, moved_col), (target_row, target_col))]
        
        for move in possible_moves:
            moved_square, target_square = move

            # Set up the original piece
            moved_piece = self.game_state.board.board[moved_square[0]][moved_square[1]]
            target_piece = self.game_state.board.board[target_square[0]][target_square[1]]

            # Suppose to do the move
            self.game_state.board.board[target_square[0]][target_square[1]] = moved_piece
            self.game_state.board.board[moved_square[0]][moved_square[1]] = '--'

            # King in check ---> INVALID move
            if not self.game_state.move_validator._in_check():
                valid_moves.append(move)

            # Reset, since this is just getting the valid moves, not do the move
            self.game_state.board.board[moved_square[0]][moved_square[1]] = moved_piece
            self.game_state.board.board[target_square[0]][target_square[1]] = target_piece

        return valid_moves


    def get_all_possible_moves(self):
        possible_moves = [] # [((moved_row, moved_col), (target_row, target_col))]

        for row in range(self.game_state.board.DIMENSION):
            for col in range(self.game_state.board.DIMENSION):
                chess_piece = self.game_state.board.board[row][col]
                if chess_piece != "--":
                    turn = chess_piece[0]
                    if (turn == 'w' and self.game_state.white_to_move) or (turn == 'b' and not self.game_state.white_to_move):
                        self.get_move_functions[chess_piece[1]](row, col, possible_moves)
        
        return possible_moves



    ####################################################################################
    # ------------------------------ GET PIECES' MOVES ---------------------------------
    ####################################################################################
    def get_sliding_moves(self, row, col, directions, possible_moves, max_steps):
        enemy_color = 'b' if self.game_state.white_to_move else 'w'

        for d_row, d_col in directions:
            # Loop runs up to max_steps (1 for King, 7 for others)
            for i in range(1, max_steps + 1):
                target_row = row + d_row * i
                target_col = col + d_col * i

                if 0 <= target_row < self.game_state.board.DIMENSION and 0 <= target_col < self.game_state.board.DIMENSION:
                    target_piece = self.game_state.board.board[target_row][target_col]
                    if target_piece == '--':
                        possible_moves.append(((row, col), (target_row, target_col)))
                    elif target_piece[0] == enemy_color:
                        possible_moves.append(((row, col), (target_row, target_col)))
                        break
                    else:
                        break
                else:
                    break


    def get_pawn_move(self, row, col, possible_moves):
        if self.game_state.white_to_move:
            if row == 0: return # pawn promotion later!

            # 1 and 2 square advanced
            if self.game_state.board.board[row - 1][col] == "--":
                possible_moves.append( ((row, col), (row - 1, col)) )
                if row == 6 and self.game_state.board.board[row - 2][col] == "--":
                    possible_moves.append( ((row, col), (row - 2, col)) )

            # Captures to the left diagonal
            if col - 1 >= 0:
                target_piece = self.game_state.board.board[row - 1][col - 1]
                if target_piece != '--' and target_piece[0] == 'b':
                    possible_moves.append( ((row, col), (row - 1, col - 1)) )

            # Captures to the right diagonal
            if col + 1 < self.game_state.board.DIMENSION:
                target_piece = self.game_state.board.board[row - 1][col + 1]
                if target_piece != '--' and target_piece[0] == 'b':
                    possible_moves.append( ((row, col), (row - 1, col + 1)) )

        else:
            if row == 7: return # pawn promotion later!

            # 1 and 2 square advance
            if self.game_state.board.board[row + 1][col] == "--":
                possible_moves.append( ((row, col), (row + 1, col)) )
                if row == 1 and self.game_state.board.board[row + 2][col] == "--":
                    possible_moves.append( ((row, col), (row + 2, col)) )
            
            # Captures to the left diagonal
            if col - 1 >= 0:
                target_piece = self.game_state.board.board[row + 1][col - 1]
                if target_piece != '--' and target_piece[0] == 'w':
                    possible_moves.append( ((row, col), (row + 1, col - 1)) )

            # Captures to the right diagonal
            if col + 1 < self.game_state.board.DIMENSION:
                target_piece = self.game_state.board.board[row + 1][col + 1]
                if target_piece != '--' and target_piece[0] == 'w':
                    possible_moves.append( ((row, col), (row + 1, col + 1)) )


    def get_rook_move(self, row, col, possible_moves):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        max_steps = self.game_state.board.DIMENSION - 1
        self.get_sliding_moves(row, col, directions, possible_moves, max_steps)


    def get_bishop_move(self, row, col, possible_moves):
        directions = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
        max_steps = self.game_state.board.DIMENSION - 1
        self.get_sliding_moves(row, col, directions, possible_moves, max_steps)

    
    def get_queen_move(self, row, col, possible_moves):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]
        max_steps = self.game_state.board.DIMENSION - 1
        self.get_sliding_moves(row, col, directions, possible_moves, max_steps)


    def get_king_move(self, row, col, possible_moves):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]
        max_steps = 1
        self.get_sliding_moves(row, col, directions, possible_moves, max_steps)


    def get_knight_move(self, row, col, possible_moves):
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        max_steps = 1
        self.get_sliding_moves(row, col, directions, possible_moves, max_steps)