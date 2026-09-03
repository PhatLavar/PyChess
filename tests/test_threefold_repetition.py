import unittest

from chess_engine import GameState
from chess_engine.moves.execution.move_executor import MoveExecutor


class ThreefoldRepetitionTests(unittest.TestCase):
    def test_third_occurrence_ends_match_as_draw(self):
        state = GameState()
        knight_cycle = (
            ((7, 6), (5, 5)),
            ((0, 6), (2, 5)),
            ((5, 5), (7, 6)),
            ((2, 5), (0, 6)),
        )

        for _ in range(2):
            for move in knight_cycle:
                self.assertEqual(
                    state.move.handle_piece_move(*move),
                    MoveExecutor.MOVED,
                )

        self.assertTrue(state.game_over)
        self.assertEqual(state.game_result, 'repetition')
        self.assertIsNone(state.winner)
        self.assertEqual(state.move.move_log[-1], '[ENDMATCH] DRAW!')
        self.assertIn('[REPETITION]', state.move.move_log[-2])

    def test_second_occurrence_does_not_end_match(self):
        state = GameState()

        for move in (
            ((7, 6), (5, 5)),
            ((0, 6), (2, 5)),
            ((5, 5), (7, 6)),
            ((2, 5), (0, 6)),
        ):
            state.move.handle_piece_move(*move)

        self.assertFalse(state.game_over)

    def test_undo_removes_the_position_from_repetition_history(self):
        state = GameState()
        state.move.handle_piece_move((7, 6), (5, 5))

        self.assertEqual(len(state.repetition_tracker.position_history), 2)
        state.move.handle_undo_move()

        self.assertEqual(len(state.repetition_tracker.position_history), 1)
        initial_key = state.repetition_tracker.position_history[0]
        self.assertEqual(state.repetition_tracker.position_counts[initial_key], 1)


if __name__ == '__main__':
    unittest.main()
