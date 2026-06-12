from chess_engine.helper import (
    DIAGONAL,
    EMP,
    KING_MOVES,
    KNIGHT_MOVES,
    ORTHOGONAL,
    enemy_color,
    in_bounds,
    piece_color,
    piece_type,
    turn_color,
)

class MoveGenerator:
    def __init__(self, game_state):
        self.game_state = game_state
        self.get_move_functions = {
            'P': self.get_pawn_move,
            'R': self.get_rook_move,
            'B': self.get_bishop_move,
            'Q': self.get_queen_move,
            'K': self.get_king_move,
            'N': self.get_knight_move,
        }

    @property
    def board(self):
        return self.game_state.board


    ####################################################################################
    # -------------------------------- GET VALID MOVES ---------------------------------
    ####################################################################################
    def get_valid_moves(self):
        valid_moves = []

        for move in self.get_all_possible_moves():
            state = self._simulate_move(move)
            if not self.game_state.move_validator._in_check():
                valid_moves.append(move)
            self._restore_move(state)

        return valid_moves

    def get_all_possible_moves(self):
        possible_moves = []
        color = turn_color(self.game_state.white_to_move)

        for row in range(self.board.DIMENSION):
            for col in range(self.board.DIMENSION):
                piece = self.board.board[row][col]
                if piece_color(piece) == color:
                    self.get_move_functions[piece_type(piece)](row, col, possible_moves)

        return possible_moves


    ####################################################################################
    # ----------------------------- VALIDATE MOVE HELPERS ------------------------------
    ####################################################################################
    def _simulate_move(self, move):
        moved_square, target_square = move
        moved_piece = self.board.get_piece(moved_square)
        target_piece = self.board.get_piece(target_square)

        state = {
            'moved_square': moved_square,
            'target_square': target_square,
            'moved_piece': moved_piece,
            'target_piece': target_piece,
            'white_king_position': self.game_state.white_king_position,
            'black_king_position': self.game_state.black_king_position,
        }

        self.board.set_piece(target_square, moved_piece)
        self.board.set_piece(moved_square, EMP)
        self._update_king_position(moved_piece, target_square)

        return state

    def _restore_move(self, state):
        self.board.set_piece(state['moved_square'], state['moved_piece'])
        self.board.set_piece(state['target_square'], state['target_piece'])
        self.game_state.white_king_position = state['white_king_position']
        self.game_state.black_king_position = state['black_king_position']

    def _update_king_position(self, piece, square):
        if piece == 'wK':
            self.game_state.white_king_position = square
        elif piece == 'bK':
            self.game_state.black_king_position = square


    ####################################################################################
    # ------------------------------ GET EACH PIECE MOVES ------------------------------
    ####################################################################################
    def get_sliding_moves(self, row, col, directions, possible_moves, max_steps):
        enemy = enemy_color(turn_color(self.game_state.white_to_move))

        for d_row, d_col in directions:
            for step in range(1, max_steps + 1):
                target = (row + d_row * step, col + d_col * step)
                if not in_bounds(target[0], target[1], self.board.DIMENSION):
                    break

                target_piece = self.board.get_piece(target)
                if target_piece == EMP:
                    possible_moves.append(((row, col), target))
                elif piece_color(target_piece) == enemy:
                    if piece_type(target_piece) != 'K':
                        possible_moves.append(((row, col), target))
                    break
                else:
                    break

    def get_pawn_move(self, row, col, possible_moves):
        color = turn_color(self.game_state.white_to_move)
        enemy = enemy_color(color)
        direction = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1
        promotion_row = 0 if color == 'w' else 7

        if row == promotion_row:
            return

        one_step = (row + direction, col)
        if self.board.get_piece(one_step) == EMP:
            possible_moves.append(((row, col), one_step))

            two_step = (row + direction * 2, col)
            if row == start_row and self.board.get_piece(two_step) == EMP:
                possible_moves.append(((row, col), two_step))

        for d_col in (-1, 1):
            target = (row + direction, col + d_col)
            if not in_bounds(target[0], target[1], self.board.DIMENSION):
                continue

            target_piece = self.board.get_piece(target)
            if piece_color(target_piece) == enemy and piece_type(target_piece) != 'K':
                possible_moves.append(((row, col), target))

    def get_rook_move(self, row, col, possible_moves):
        self.get_sliding_moves(row, col, ORTHOGONAL, possible_moves, self.board.DIMENSION - 1)

    def get_bishop_move(self, row, col, possible_moves):
        self.get_sliding_moves(row, col, DIAGONAL, possible_moves, self.board.DIMENSION - 1)

    def get_queen_move(self, row, col, possible_moves):
        self.get_sliding_moves(row, col, ORTHOGONAL + DIAGONAL, possible_moves, self.board.DIMENSION - 1)

    def get_king_move(self, row, col, possible_moves):
        self.get_sliding_moves(row, col, KING_MOVES, possible_moves, 1)

    def get_knight_move(self, row, col, possible_moves):
        self.get_sliding_moves(row, col, KNIGHT_MOVES, possible_moves, 1)
