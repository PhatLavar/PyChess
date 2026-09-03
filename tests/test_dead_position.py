import unittest

from chess_engine import GameState
from chess_engine.utilities import EMP


class DeadPositionTests(unittest.TestCase):
    def _state_with_pieces(self, pieces):
        state = GameState()
        state.board.board = [[EMP for _ in range(8)] for _ in range(8)]
        state.board.set_piece((7, 4), 'wK')
        state.board.set_piece((0, 4), 'bK')
        state.white_king_position = (7, 4)
        state.black_king_position = (0, 4)

        for square, piece in pieces:
            state.board.set_piece(square, piece)

        return state

    def test_bare_kings_end_as_dead_position_draw(self):
        state = self._state_with_pieces([])

        move_status, match_result = state.finish_turn()

        self.assertEqual(move_status, 'DEAD_POSITION')
        self.assertEqual(match_result, 'DRAW!')
        self.assertTrue(state.game_over)
        self.assertEqual(state.game_result, 'dead_position')
        self.assertIsNone(state.winner)

    def test_single_minor_piece_against_king_is_dead(self):
        for piece in ('wB', 'wN'):
            with self.subTest(piece=piece):
                state = self._state_with_pieces([((4, 4), piece)])
                self.assertTrue(
                    state.dead_position_validator.is_dead_position()
                )

    def test_bishops_on_same_square_color_are_dead(self):
        state = self._state_with_pieces([
            ((6, 2), 'wB'),
            ((3, 5), 'bB'),
        ])

        self.assertTrue(state.dead_position_validator.is_dead_position())

    def test_opposite_colored_bishops_are_not_automatically_dead(self):
        state = self._state_with_pieces([
            ((6, 2), 'wB'),
            ((3, 4), 'bB'),
        ])

        self.assertFalse(state.dead_position_validator.is_dead_position())

    def test_pawn_or_two_knights_can_still_allow_mate(self):
        for pieces in (
            [((4, 4), 'wP')],
            [((4, 4), 'wN'), ((3, 2), 'wN')],
        ):
            with self.subTest(pieces=pieces):
                state = self._state_with_pieces(pieces)
                self.assertFalse(
                    state.dead_position_validator.is_dead_position()
                )


if __name__ == '__main__':
    unittest.main()
