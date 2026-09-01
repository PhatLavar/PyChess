import random
import unittest

from chess_engine import GameState
from chess_engine.bots import BaseBot, HardBot
from chess_engine.utilities import EMP


class HardBotTests(unittest.TestCase):
    def test_hard_bot_uses_common_bot_interface_and_three_ply_search(self):
        bot = HardBot()

        self.assertIsInstance(bot, BaseBot)
        self.assertEqual(bot.depth, 3)

    def test_chosen_move_is_legal_in_sparse_position(self):
        state = self._sparse_state()
        state.board.set_piece((6, 3), 'wQ')
        state.board.set_piece((1, 3), 'bR')
        bot = HardBot(rng=random.Random(7))

        self.assertIn(bot.choose_move(state), state.move.get_valid_moves())

    def test_hard_bot_takes_an_undefended_queen(self):
        state = self._sparse_state()
        state.board.set_piece((4, 0), 'wR')
        state.board.set_piece((4, 5), 'bQ')
        bot = HardBot(rng=random.Random(7))

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
