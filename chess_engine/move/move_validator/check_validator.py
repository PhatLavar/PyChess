from chess_engine.helpers import enemy_color, turn_color


class CheckValidator:
    def __init__(self, game_state, attack_validator):
        self.game_state = game_state
        self.attack_validator = attack_validator

    def find_king(self, color=None):
        if color is None:
            color = turn_color(self.game_state.white_to_move)

        return (
            self.game_state.white_king_position
            if color == 'w'
            else self.game_state.black_king_position
        )

    def in_check(self, color=None):
        if color is None:
            color = turn_color(self.game_state.white_to_move)

        king_position = self.find_king(color)
        enemy = enemy_color(color)

        return self.attack_validator.square_under_attack(king_position, enemy)

    def is_checkmate(self):
        valid_moves = self.game_state.move.get_valid_moves()
        return len(valid_moves) == 0 and self.in_check()

    def is_stalemate(self):
        valid_moves = self.game_state.move.get_valid_moves()
        return len(valid_moves) == 0 and not self.in_check()