import random
import unittest
from threading import Event
from unittest.mock import patch

from chess_app.chess_game import ChessGame
from chess_engine import GameState
from chess_engine.bots import EasyBot, HardBot, ImpossibleBot, MasterBot, MediumBot


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
    def finish_bot_turn(self):
        self.assertFalse(self.game._play_bot_turn())
        self.game._bot_task[0].result(timeout=5)
        return self.game._play_bot_turn()

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

    def test_impossible_selection_enables_impossible_bot(self):
        with patch.object(self.game, '_create_match'):
            self.game.start_bot_game('impossible')

        self.assertIsInstance(self.game.bot, ImpossibleBot)
        self.assertEqual(self.game.bot_difficulty, 'impossible')

    def test_easy_bot_plays_black_after_white_move(self):
        outcome = self.game.game_state.move.handle_piece_move((6, 4), (4, 4))

        self.assertEqual(outcome, 'moved')
        self.assertTrue(self.game.is_bot_turn)
        with patch('chess_app.chess_game.pg.time.get_ticks', side_effect=[1000, 1499, 1500, 1501]):
            self.assertFalse(self.game._play_bot_turn())
            self.assertFalse(self.game._play_bot_turn())
            self.assertTrue(self.finish_bot_turn())
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
        with patch('chess_app.chess_game.pg.time.get_ticks', side_effect=[1000, 1500, 1501]):
            self.game._play_bot_turn()
            self.finish_bot_turn()

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

    def test_bot_bot_selection_creates_same_difficulty_for_both_colors(self):
        self.game.white_bot = None

        with patch.object(self.game, '_create_match'):
            self.game.start_bot_bot_game('hard')

        self.assertEqual(self.game.gamemode, ChessGame.BOT_BOT_MODE)
        self.assertEqual(self.game.bot_difficulty, 'hard')
        self.assertIsInstance(self.game.white_bot, HardBot)
        self.assertIsInstance(self.game.bot, HardBot)
        self.assertIsNot(self.game.white_bot, self.game.bot)

    def test_bot_bot_mode_automatically_plays_both_colors(self):
        self.game.gamemode = ChessGame.BOT_BOT_MODE
        self.game.white_bot = EasyBot(rng=random.Random(3))

        with patch(
            'chess_app.chess_game.pg.time.get_ticks',
            side_effect=[1000, 1500, 1501, 2000, 2500, 2501],
        ):
            self.assertFalse(self.game._play_bot_turn())
            self.assertTrue(self.finish_bot_turn())
            self.assertFalse(self.game._play_bot_turn())
            self.assertTrue(self.finish_bot_turn())

        self.assertTrue(self.game.game_state.white_to_move)
        self.assertEqual(len(self.game.game_state.move.notation), 2)
        self.assertEqual(self.game.input_handler.animation_count, 2)

    def test_bot_bot_mode_does_not_allow_undo(self):
        self.game.gamemode = ChessGame.BOT_BOT_MODE
        self.game.white_bot = EasyBot(rng=random.Random(3))

        self.assertFalse(self.game.handle_undo())
        self.assertEqual(self.game.input_handler.undo_count, 0)

    def test_thinking_does_not_block_and_undo_discards_result(self):
        entered, release = Event(), Event()
        def think(snapshot):
            self.assertIsNot(snapshot, self.game.game_state)
            entered.set()
            release.wait(5)
            return ((1, 4), (3, 4))

        self.game.game_state.move.handle_piece_move((6, 4), (4, 4))
        self.game.bot_wait_started_at = 0
        with patch.object(self.game.bot, 'choose_move', side_effect=think), patch(
            'chess_app.chess_game.pg.time.get_ticks', return_value=2000
        ):
            try:
                self.assertFalse(self.game._play_bot_turn())
                self.assertTrue(entered.wait(2))
                self.assertFalse(self.game._play_bot_turn())
                self.assertTrue(self.game.handle_undo())
            finally:
                release.set()
            self.game._bot_task[0].result(timeout=2)
            self.game.game_state.move.handle_piece_move((6, 3), (4, 3))
            self.game.bot_wait_started_at = 0
            self.assertFalse(self.game._play_bot_turn())
            self.assertEqual(len(self.game.game_state.move.notation), 1)


if __name__ == '__main__':
    unittest.main()
