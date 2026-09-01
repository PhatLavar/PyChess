import random
import unittest

from chess_engine import GameState
from chess_engine.bots import BaseBot, MediumBot
from chess_engine.utilities import EMP


class MediumBotTests(unittest.TestCase):
    def test_medium_bot_uses_common_bot_interface(self):
        self.assertIsInstance(MediumBot(), BaseBot)

    def test_chosen_opening_move_is_legal(self):
        state = GameState()
        bot = MediumBot(rng=random.Random(7))

        self.assertIn(bot.choose_move(state), state.move.get_valid_moves())

    def test_bot_avoids_losing_its_queen(self):
        state = GameState()
        state.board.board = [[EMP for _ in range(8)] for _ in range(8)]
        state.board.set_piece((7, 4), 'wK')
        state.board.set_piece((0, 4), 'bK')
        state.board.set_piece((4, 3), 'wQ')
        state.board.set_piece((3, 3), 'bR')
        state.white_king_position = (7, 4)
        state.black_king_position = (0, 4)
        state.castling_rights = {
            'w': {'king_side': False, 'queen_side': False},
            'b': {'king_side': False, 'queen_side': False},
        }
        bot = MediumBot(rng=random.Random(7))

        move = bot.choose_move(state)

        self.assertEqual(move, ((4, 3), (3, 3)))


if __name__ == '__main__':
    unittest.main()
