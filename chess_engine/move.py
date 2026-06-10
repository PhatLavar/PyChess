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
    def handle_selected_piece_move(self, moved_square, target_square):
        if self.game_state.moved_piece == '--':
            self.game_state.selected_square = ()
            self.game_state.player_clicked = []
            return
        
        valid_moves = self.get_valid_moves()
        current_move = (moved_square, target_square)

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
        
        if current_move not in valid_moves:
            self.record_move(self.game_state.moved_piece, moved_square, self.game_state.target_piece, target_square, move_type='INVALID')
            self.game_state.selected_square = ()
            self.game_state.player_clicked = []
            return

        capture = self.game_state.target_piece != '--'
        self.game_state.board.board[target_square[0]][target_square[1]] = self.game_state.moved_piece
        self.game_state.board.board[moved_square[0]][moved_square[1]] = '--'

        # record the move and save undo metadata
        self.record_move(self.game_state.moved_piece, moved_square, self.game_state.target_piece, target_square, move_type='MOVE')
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
    def square_to_notation(self, square):
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

        from_notation = self.square_to_notation(moved_square)
        to_notation = self.square_to_notation(target_square)

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

        if len(self.move_log) > 0:
            self.move_log.pop()

        self.record_move(moved_piece, target_square, target_prev_piece, moved_square, move_type='REDO')

        self.game_state.selected_square = ()
        self.game_state.player_clicked = []
        self.game_state.white_to_move = not self.game_state.white_to_move



    ####################################################################################
    # ----------------------------- GET ALL VALID MOVES --------------------------------
    ####################################################################################
    def get_valid_moves(self):
        valid_moves = [] # [((moved_row, moved_col), (target_row, target_col))]
        return self.get_all_possible_moves() # we won't consider the check after moving! (yet)


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

            #Captures to the left diagonal
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
        pass