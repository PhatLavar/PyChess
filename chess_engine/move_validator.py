from chess_engine.helper import (
    DIAGONAL,
    EMP,
    KING_MOVES,
    KNIGHT_MOVES,
    ORTHOGONAL,

    CASTLING_KING_START,
    CASTLING_ROOK_START,

    enemy_color,
    in_bounds,
    piece_color,
    piece_type,
    turn_color,
    get_promotion_row
)


class MoveValidator:
    def __init__(self, game_state):
        self.game_state = game_state

    @property
    def board(self):
        return self.game_state.board

    def _find_king(self, color=None):
        if color is None: color = turn_color(self.game_state.white_to_move)
        return self.game_state.white_king_position if color == 'w' else self.game_state.black_king_position

    def _get_enemy_color(self, color=None):
        if color is None: color = turn_color(self.game_state.white_to_move)
        return enemy_color(color)

    def _in_bounds(self, row, col):
        return in_bounds(row, col, self.board.DIMENSION)


    ####################################################################################
    # ------------- CHECK IF A SQUARE IS UNDER ATTACK BY OPPONENT PIECES ---------------
    ####################################################################################
    def _square_under_attack(self, square, enemy_color):
        row, col = square

        pawn_direction = 1 if enemy_color == 'w' else -1
        for d_col in (-1, 1):
            attack_row = row + pawn_direction
            attack_col = col + d_col
            if self._in_bounds(attack_row, attack_col):
                piece = self.board.get_piece((attack_row, attack_col))
                if piece == enemy_color + 'P':
                    return True

        if self._attacked_by_step_piece(row, col, enemy_color, KNIGHT_MOVES, 'N'): return True
        if self._attacked_by_step_piece(row, col, enemy_color, KING_MOVES, 'K'): return True
        if self._attacked_by_sliding_piece(row, col, enemy_color, ORTHOGONAL, ('R', 'Q')): return True
        if self._attacked_by_sliding_piece(row, col, enemy_color, DIAGONAL, ('B', 'Q')): return True
        return False

    def _attacked_by_step_piece(self, row, col, enemy, directions, attacker_type):
        for d_row, d_col in directions:
            attack_row = row + d_row
            attack_col = col + d_col
            if self._in_bounds(attack_row, attack_col):
                piece = self.board.get_piece((attack_row, attack_col))
                if piece == enemy + attacker_type:
                    return True
        return False

    def _attacked_by_sliding_piece(self, row, col, enemy_color, directions, valid_piece_types):
        for d_row, d_col in directions:
            attack_row = row + d_row
            attack_col = col + d_col

            while self._in_bounds(attack_row, attack_col):
                piece = self.board.get_piece((attack_row, attack_col))
                if piece == EMP:
                    attack_row += d_row
                    attack_col += d_col
                    continue
                if piece_color(piece) == enemy_color and piece_type(piece) in valid_piece_types:
                    return True
                break

        return False


    ####################################################################################
    # ------------------- CHECK IF A PIECE IS PINNED (CANNOT MOVE) ---------------------
    ####################################################################################
    def _is_pinned(self, square, color=None):
        if color is None:
            color = turn_color(self.game_state.white_to_move)

        row, col = square
        piece = self.board.get_piece(square)
        if piece == EMP or piece_color(piece) != color or piece_type(piece) == 'K':
            return False

        self.board.set_piece(square, EMP)
        is_pinned = self._in_check(color)
        self.board.set_piece(square, piece)

        return is_pinned


    ####################################################################################
    # --------------- CHECK IF KING IS CHECKED AFTER STIMULATE THE MOVE ----------------
    ####################################################################################
    def _in_check(self, color=None):
        if color is None:
            color = turn_color(self.game_state.white_to_move)

        king_position = self._find_king(color)
        enemy_color = self._get_enemy_color(color)
        return self._square_under_attack(king_position, enemy_color)


    def in_check(self, color=None):
        return self._in_check(color)


    ####################################################################################
    # ---------------------------- CHECKMATE, STALEMATE --------------------------------
    ####################################################################################
    def is_checkmate(self):
        valid_move = self.game_state.move.get_valid_moves()
        return len(valid_move) == 0 and self._in_check()


    def is_stalemate(self):
        valid_move = self.game_state.move.get_valid_moves()
        return len(valid_move) == 0 and not self._in_check()
    

    ####################################################################################
    # ------------------ CHECK IF PAWN CAN BE PROMOTED AFTER THE MOVE ------------------
    ####################################################################################
    def can_pawn_promotion(self, target_square):
        return get_promotion_row(self.game_state.white_to_move) == target_square[0]


    ####################################################################################
    # -------------------- CHECK IF PAWN MOVE IS AN EN PASSANT MOVE --------------------
    ####################################################################################
    def is_en_passant_move(self, moved_piece, moved_square, target_square):
        return (
            moved_piece[1] == 'P'
            and target_square == self.game_state.en_passant_target
            and self.board.get_piece(target_square) == EMP
            and moved_square[1] != target_square[1]
            and self.game_state.last_double_pawn_move is not None
        )


    ####################################################################################
    # --------------------- CHECK IF KING MOVE IS A CASTLING MOVE ----------------------
    ####################################################################################
    def is_castling_move(self, moved_piece, moved_square, target_square):
        return (
            moved_piece[1] == 'K'
            and abs(target_square[1] - moved_square[1]) == 2
        )
    
    
    ####################################################################################
    # ---------------------------- CHECK IF KING CAN CASTLE ----------------------------
    ####################################################################################
    def can_castle(self, color, side):
        rights = self.game_state.castling_rights[color]
        if not rights[side]:
            return False
        
        king_start = CASTLING_KING_START[color]
        rook_start = CASTLING_ROOK_START[color][side]

        king = self.board.get_piece(king_start)
        rook = self.board.get_piece(rook_start)

        if king != color + 'K': return False
        if rook != color + 'R': return False
        if self._in_check(color): return False
        if not self._castling_path_empty(color, side): return False
        if self._castling_path_under_attack(color, side): return False

        return True
    

    def _castling_path_empty(self, color, side):
        row = 7 if color == 'w' else 0

        if side == 'king_side':
            squares = [(row, 5), (row, 6)]
        else:
            squares = [(row, 1), (row, 2), (row, 3)]

        return all(self.board.get_piece(square) == EMP for square in squares)


    def _castling_path_under_attack(self, color, side):
        row = 7 if color == 'w' else 0
        enemy = enemy_color(color)

        if side == 'king_side':
            king_path = [(row, 5), (row, 6)]
        else:
            king_path = [(row, 3), (row, 2)]

        return any(self._square_under_attack(square, enemy) for square in king_path)