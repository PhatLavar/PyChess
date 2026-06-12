from chess_engine.move_executor import MoveExecutor
from chess_engine.move_generator import MoveGenerator
from chess_engine.move_logger import MoveLogger

class Move:
    def __init__(self, game_state):
        self.game_state = game_state
        self.generator = MoveGenerator(game_state)
        self.logger = MoveLogger(game_state.board)
        self.executor = MoveExecutor(game_state, self.generator, self.logger)

    @property
    def move_log(self):
        return self.logger.move_log

    @property
    def notation(self):
        return self.logger.notation

    def handle_piece_move(self, moved_square, target_square):
        self.executor.handle_piece_move(moved_square, target_square)

    def handle_undo_move(self):
        self.executor.handle_undo_move()

    def get_valid_moves(self):
        return self.generator.get_valid_moves()

    def get_all_possible_moves(self):
        return self.generator.get_all_possible_moves()

    def record_move(self, moved_piece, moved_square, target_piece, target_square, move_type='MOVE'):
        self.logger.record_move(moved_piece, moved_square, target_piece, target_square, move_type)
