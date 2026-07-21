from chess_engine.helpers import get_promotion_row


class PromotionValidator:
    def __init__(self, game_state):
        self.game_state = game_state

    def can_pawn_promotion(self, target_square):
        return get_promotion_row(self.game_state.white_to_move) == target_square[0]