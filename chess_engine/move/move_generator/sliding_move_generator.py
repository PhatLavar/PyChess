from chess_engine.helpers import (
    EMP,
    ORTHOGONAL,
    DIAGONAL,
    enemy_color,
    in_bounds,
    piece_color,
    piece_type,
    turn_color,
)


class SlidingMoveGenerator:
    def __init__(self, game_state):
        self.game_state = game_state

    @property
    def board(self):
        return self.game_state.board

    def generate_rook(self, row, col, possible_moves):
        self._generate(row, col, ORTHOGONAL, possible_moves, self.board.DIMENSION - 1)

    def generate_bishop(self, row, col, possible_moves):
        self._generate(row, col, DIAGONAL, possible_moves, self.board.DIMENSION - 1)

    def generate_queen(self, row, col, possible_moves):
        self._generate(row, col, ORTHOGONAL + DIAGONAL, possible_moves, self.board.DIMENSION - 1)

    def _generate(self, row, col, directions, possible_moves, max_steps):
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