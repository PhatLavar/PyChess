from chess_engine.utilities import get_promotion_row


class PromotionValidator:
    """
    Detect when a pawn reaches its promotion rank.
    """

    def __init__(self, game_state):
        """
        Bind the active match state.
        """
        self.game_state = game_state

    def can_pawn_promotion(self, target_square):
        """
        Return whether the target square is side to move's promotion row.
        """
        return get_promotion_row(self.game_state.white_to_move) == target_square[0]
