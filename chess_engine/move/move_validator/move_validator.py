from chess_engine.move.move_validator.attack_validator import AttackValidator
from chess_engine.move.move_validator.check_validator import CheckValidator
from chess_engine.move.move_validator.castling_validator import CastlingValidator
from chess_engine.move.move_validator.en_passant_validator import EnPassantValidator
from chess_engine.move.move_validator.pawn_promotion_validator import PromotionValidator


class MoveValidator:
    def __init__(self, game_state):
        self.game_state = game_state

        self.attack_validator = AttackValidator(game_state)
        self.check_validator = CheckValidator(game_state, self.attack_validator)
        self.castling_validator = CastlingValidator(game_state, self.attack_validator)
        self.en_passant_validator = EnPassantValidator(game_state)
        self.promotion_validator = PromotionValidator(game_state)

    def _square_under_attack(self, square, enemy_color):
        return self.attack_validator.square_under_attack(square, enemy_color)

    def _in_check(self, color=None):
        return self.check_validator.in_check(color)

    def in_check(self, color=None):
        return self.check_validator.in_check(color)

    def is_checkmate(self):
        return self.check_validator.is_checkmate()

    def is_stalemate(self):
        return self.check_validator.is_stalemate()

    def can_pawn_promotion(self, target_square):
        return self.promotion_validator.can_pawn_promotion(target_square)

    def is_en_passant_move(self, moved_piece, moved_square, target_square):
        return self.en_passant_validator.is_en_passant_move(
            moved_piece,
            moved_square,
            target_square
        )

    def is_castling_move(self, moved_piece, moved_square, target_square):
        return self.castling_validator.is_castling_move(
            moved_piece,
            moved_square,
            target_square
        )

    def can_castle(self, color, side):
        return self.castling_validator.can_castle(color, side)