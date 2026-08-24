from chess_engine.core.board import Board
from chess_engine.moves import Move
from chess_engine.rules import MoveValidator


class GameState:
    """Store all rules-related state for one chess match.

    This class intentionally has no Pygame, rendering, animation, or input
    dependencies, so the same engine can later be used by an AI player.
    """

    WHITE_KING_START = (7, 4)
    BLACK_KING_START = (0, 4)

    def __init__(self):
        """Create a fresh match with White to move."""
        self.white_to_move = True
        self.board = Board()

        self.white_king_position = self.WHITE_KING_START
        self.black_king_position = self.BLACK_KING_START

        self.promotion_pending = False
        self.promotion_square = None
        self.promotion_moved_square = None
        self.promotion_moved_piece = None
        self.promotion_target_piece = None
        self.promotion_color = None

        self.en_passant_target = None
        self.last_double_pawn_move = None

        self.castling_rights = {
            'w': {'king_side': True, 'queen_side': True},
            'b': {'king_side': True, 'queen_side': True},
        }
        self.castling_rights_log = []

        self.game_over = False
        self.game_result = None
        self.winner = None

        self.move_validator = MoveValidator(self)
        self.move = Move(self)

    # Match state

    def finish_turn(self):
        """Switch turns and evaluate the resulting position.

        Returns:
            A ``(move_status, match_result)`` tuple. ``move_status`` is
            ``CHECK``, ``CHECKMATE``, ``STALEMATE``, or ``None``.
            ``match_result`` is ``WHITE WINS!``, ``BLACK WINS!``, ``DRAW!``,
            or ``None`` when the match continues.
        """
        self.white_to_move = not self.white_to_move

        if self.move_validator.is_checkmate():
            winner = 'BLACK WINS!' if self.white_to_move else 'WHITE WINS!'
            self._set_game_over(result='checkmate', winner=winner)
            return 'CHECKMATE', winner

        if self.move_validator.is_stalemate():
            self._set_game_over(result='stalemate', winner=None)
            return 'STALEMATE', 'DRAW!'

        if self.move_validator.in_check():
            return 'CHECK', None

        return None, None

    def get_terminal_king_square(self):
        """Return the side-to-move king square for the endgame animation."""
        if self.white_to_move:
            return self.white_king_position
        return self.black_king_position

    def _set_game_over(self, result, winner):
        """Lock the match and store its terminal result."""
        self.game_over = True
        self.game_result = result
        self.winner = winner
