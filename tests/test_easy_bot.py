import random
import unittest

from chess_engine import GameState
from chess_engine.bots import BaseBot, EasyBot
from chess_engine.utilities import EMP


class EasyBotTests(unittest.TestCase):
    def test_easy_bot_uses_common_bot_interface(self):
        self.assertIsInstance(EasyBot(), BaseBot)

    def test_chosen_opening_move_is_legal(self):
        state = GameState()
        bot = EasyBot(rng=random.Random(7))

        move = bot.choose_move(state)

        self.assertIn(move, state.move.get_valid_moves())

    def test_bot_prefers_a_free_queen_capture(self):
        state = GameState()
        state.board.board = [[EMP for _ in range(8)] for _ in range(8)]
        state.board.set_piece((7, 4), 'wK')
        state.board.set_piece((0, 4), 'bK')
        state.board.set_piece((4, 0), 'wR')
        state.board.set_piece((4, 5), 'bQ')
        state.white_king_position = (7, 4)
        state.black_king_position = (0, 4)
        state.castling_rights = {
            'w': {'king_side': False, 'queen_side': False},
            'b': {'king_side': False, 'queen_side': False},
        }
        bot = EasyBot(rng=random.Random(7))

        self.assertEqual(bot.choose_move(state), ((4, 0), (4, 5)))

    def test_no_legal_moves_returns_none(self):
        state = GameState()
        state.move.get_valid_moves = lambda: []

        self.assertIsNone(EasyBot().choose_move(state))


if __name__ == '__main__':
    unittest.main()
