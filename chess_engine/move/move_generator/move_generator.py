from chess_engine.helpers import piece_color, piece_type, turn_color
from chess_engine.move.move_generator.move_simulation import MoveSimulation
from chess_engine.move.move_generator.sliding_move_generator import SlidingMoveGenerator
from chess_engine.move.move_generator.pawn_move_generator import PawnMoveGenerator
from chess_engine.move.move_generator.king_move_generator import KingMoveGenerator
from chess_engine.move.move_generator.knight_move_generator import KnightMoveGenerator


class MoveGenerator:
    def __init__(self, game_state):
        self.game_state = game_state
        self.simulation = MoveSimulation(game_state)
        self.sliding_generator = SlidingMoveGenerator(game_state)
        self.pawn_generator = PawnMoveGenerator(game_state)
        self.king_generator = KingMoveGenerator(game_state)
        self.knight_generator = KnightMoveGenerator(game_state)

    @property
    def board(self):
        return self.game_state.board

    def get_valid_moves(self):
        valid_moves = []

        for move in self.get_all_possible_moves():
            state = self.simulation.simulate(move)

            if not self.game_state.move_validator._in_check():
                valid_moves.append(move)

            self.simulation.restore(state)

        return valid_moves

    def get_all_possible_moves(self):
        possible_moves = []
        color = turn_color(self.game_state.white_to_move)

        for row in range(self.board.DIMENSION):
            for col in range(self.board.DIMENSION):
                piece = self.board.board[row][col]

                if piece_color(piece) == color:
                    self._generate_piece_moves(row, col, piece, possible_moves)

        return possible_moves

    def _generate_piece_moves(self, row, col, piece, possible_moves):
        move_type = piece_type(piece)

        if move_type == 'P':
            self.pawn_generator.generate(row, col, possible_moves)
        elif move_type == 'R':
            self.sliding_generator.generate_rook(row, col, possible_moves)
        elif move_type == 'B':
            self.sliding_generator.generate_bishop(row, col, possible_moves)
        elif move_type == 'Q':
            self.sliding_generator.generate_queen(row, col, possible_moves)
        elif move_type == 'K':
            self.king_generator.generate(row, col, possible_moves)
        elif move_type == 'N':
            self.knight_generator.generate(row, col, possible_moves)