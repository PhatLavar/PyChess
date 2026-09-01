import random
import unittest

from chess_engine import GameState
from chess_engine.bots import BaseBot, MasterBot
from chess_engine.utilities import EMP


class MasterBotTests(unittest.TestCase):
    def test_master_bot_has_deterministic_extended_tactical_search(self):
        bot = MasterBot()

        self.assertIsInstance(bot, BaseBot)
        self.assertEqual(bot.depth, 2)
        self.assertEqual(bot.choice_window, 0)
        self.assertEqual(bot.quiescence_depth, 2)

    def test_master_bot_selects_a_legal_tactical_move(self):
        state = self._sparse_state()
        state.board.set_piece((4, 0), 'wR')
        state.board.set_piece((4, 5), 'bQ')
        bot = MasterBot(rng=random.Random(7))

        self.assertEqual(bot.choose_move(state), ((4, 0), (4, 5)))

    def _sparse_state(self):
        state = GameState()
        state.board.board = [[EMP for _ in range(8)] for _ in range(8)]
        state.board.set_piece((7, 4), 'wK')
        state.board.set_piece((0, 4), 'bK')
        state.white_king_position = (7, 4)
        state.black_king_position = (0, 4)
        state.castling_rights = {
            'w': {'king_side': False, 'queen_side': False},
            'b': {'king_side': False, 'queen_side': False},
        }
        return state


if __name__ == '__main__':
    unittest.main()
