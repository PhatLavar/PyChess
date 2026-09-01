import random
import unittest
from unittest.mock import patch

from chess_app.chess_game import ChessGame
from chess_engine import GameState
from chess_engine.bots import EasyBot, HardBot, MasterBot, MediumBot


class AnimationStub:
    is_animating = False


class InputStub:
    def __init__(self, game_state=None):
        self.game_state = game_state
        self.animation_count = 0
        self.undo_count = 0

    def animate_latest_move(self):
        self.animation_count += 1

    def handle_undo(self):
        changed = self.game_state.move.handle_undo_move()
        if changed:
            self.undo_count += 1
        return changed


class BotGameplayTests(unittest.TestCase):
    def setUp(self):
        self.game = ChessGame.__new__(ChessGame)
        self.game.gamemode = ChessGame.BOT_MODE
        self.game.bot_difficulty = 'easy'
        self.game.bot = EasyBot(rng=random.Random(7))
        self.game.bot_wait_started_at = None
        self.game.game_state = GameState()
        self.game.move_animation = AnimationStub()
        self.game.input_handler = InputStub(self.game.game_state)

    def test_player_starts_as_white(self):
        self.assertTrue(self.game.game_state.white_to_move)
        self.assertFalse(self.game.is_bot_turn)

    def test_medium_selection_enables_medium_bot(self):
        with patch.object(self.game, '_create_match'):
            self.game.start_bot_game('medium')

        self.assertIsInstance(self.game.bot, MediumBot)
        self.assertEqual(self.game.bot_difficulty, 'medium')

    def test_hard_selection_enables_hard_bot(self):
        with patch.object(self.game, '_create_match'):
            self.game.start_bot_game('hard')

        self.assertIsInstance(self.game.bot, HardBot)
        self.assertEqual(self.game.bot_difficulty, 'hard')

    def test_master_selection_enables_master_bot(self):
        with patch.object(self.game, '_create_match'):
            self.game.start_bot_game('master')

        self.assertIsInstance(self.game.bot, MasterBot)
        self.assertEqual(self.game.bot_difficulty, 'master')

    def test_easy_bot_plays_black_after_white_move(self):
        outcome = self.game.game_state.move.handle_piece_move((6, 4), (4, 4))

        self.assertEqual(outcome, 'moved')
        self.assertTrue(self.game.is_bot_turn)
        with patch('chess_app.chess_game.pg.time.get_ticks', side_effect=[1000, 1499, 1500]):
            self.assertFalse(self.game._play_bot_turn())
            self.assertFalse(self.game._play_bot_turn())
            self.assertTrue(self.game._play_bot_turn())
        self.assertTrue(self.game.game_state.white_to_move)
        self.assertEqual(len(self.game.game_state.move.notation), 2)
        self.assertEqual(self.game.input_handler.animation_count, 1)

    def test_bot_waits_for_player_animation(self):
        self.game.game_state.move.handle_piece_move((6, 4), (4, 4))
        self.game.move_animation.is_animating = True

        self.assertFalse(self.game._play_bot_turn())
        self.assertFalse(self.game.game_state.white_to_move)

    def test_undo_after_bot_reply_restores_position_before_player_move(self):
        initial_board = [row.copy() for row in self.game.game_state.board.board]
        self.game.game_state.move.handle_piece_move((6, 4), (4, 4))
        with patch('chess_app.chess_game.pg.time.get_ticks', side_effect=[1000, 1500]):
            self.game._play_bot_turn()
            self.game._play_bot_turn()

        self.assertTrue(self.game.handle_undo())
        self.assertEqual(self.game.input_handler.undo_count, 2)
        self.assertEqual(self.game.game_state.board.board, initial_board)
        self.assertTrue(self.game.game_state.white_to_move)

    def test_undo_before_bot_reply_cancels_pending_bot_turn(self):
        initial_board = [row.copy() for row in self.game.game_state.board.board]
        self.game.game_state.move.handle_piece_move((6, 4), (4, 4))
        self.game.bot_wait_started_at = 1000

        self.assertTrue(self.game.handle_undo())
        self.assertEqual(self.game.input_handler.undo_count, 1)
        self.assertEqual(self.game.game_state.board.board, initial_board)
        self.assertTrue(self.game.game_state.white_to_move)
        self.assertIsNone(self.game.bot_wait_started_at)


if __name__ == '__main__':
    unittest.main()
