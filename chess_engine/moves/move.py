from chess_engine.moves.execution import MoveExecutor
from chess_engine.moves.generation import MoveGenerator
from chess_engine.moves.history import MoveLogger

class Move:
    """
    Expose move generation, execution, history, and undo through one API.
    """

    def __init__(self, game_state):
        """
        Create generation, execution, and history services.
        """
        self.game_state = game_state
        self.generator = MoveGenerator(game_state)
        self.logger = MoveLogger(game_state.board)
        self.executor = MoveExecutor(game_state, self.generator, self.logger)

    @property
    def move_log(self):
        """
        Return human-readable move log entries.
        """
        return self.logger.move_log

    @property
    def notation(self):
        """
        Return structured move records used by undo and future notation.
        """
        return self.logger.notation

    def handle_piece_move(self, moved_square, target_square):
        """
        Attempt a move and return the executor's named outcome.
        """
        return self.executor.handle_piece_move(moved_square, target_square)

    def handle_undo_move(self):
        """
        Undo the latest move and return whether state changed.
        """
        return self.executor.handle_undo_move()

    def get_valid_moves(self):
        """
        Return all legal moves for side to move.
        """
        return self.generator.get_valid_moves()

    def get_all_possible_moves(self):
        """
        Return pseudo-legal moves before own-king safety filtering.
        """
        return self.generator.get_all_possible_moves()

    def record_move(self, moved_piece, moved_square, target_piece, target_square, move_type='MOVE'):
        """
        Append a human-readable move entry and return no value.
        """
        self.logger.record_move(moved_piece, moved_square, target_piece, target_square, move_type)
