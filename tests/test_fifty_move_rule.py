import unittest

from chess_engine import GameState
from chess_engine.moves.execution.move_executor import MoveExecutor


class FiftyMoveRuleTests(unittest.TestCase):
    def test_hundredth_halfmove_ends_match_as_draw(self):
        state = GameState()
        state.fifty_move_rule.halfmove_clock = 99

        result = state.move.handle_piece_move((7, 6), (5, 5))

        self.assertEqual(result, MoveExecutor.MOVED)
        self.assertTrue(state.game_over)
        self.assertEqual(state.game_result, 'fifty_move')
        self.assertIsNone(state.winner)
        self.assertEqual(state.move.move_log[-1], '[ENDMATCH] DRAW!')
        self.assertIn('[FIFTY_MOVE]', state.move.move_log[-2])

    def test_pawn_move_resets_halfmove_clock(self):
        state = GameState()
        state.fifty_move_rule.halfmove_clock = 99

        state.move.handle_piece_move((6, 4), (4, 4))

        self.assertEqual(state.fifty_move_rule.halfmove_clock, 0)
        self.assertFalse(state.game_over)

    def test_capture_resets_halfmove_clock(self):
        state = GameState()
        state.fifty_move_rule.halfmove_clock = 99
        state.board.set_piece((5, 5), 'bB')

        state.move.handle_piece_move((7, 6), (5, 5))

        self.assertEqual(state.fifty_move_rule.halfmove_clock, 0)
        self.assertFalse(state.game_over)

    def test_undo_restores_previous_halfmove_clock(self):
        state = GameState()
        state.fifty_move_rule.halfmove_clock = 42
        state.move.handle_piece_move((7, 6), (5, 5))

        self.assertEqual(state.fifty_move_rule.halfmove_clock, 43)
        state.move.handle_undo_move()

        self.assertEqual(state.fifty_move_rule.halfmove_clock, 42)


if __name__ == '__main__':
    unittest.main()
