import random
import unittest

from chess_app.chess_game import ChessGame
from chess_engine import GameState
from chess_engine.bots import EasyBot


class AnimationStub:
    is_animating = False


class InputStub:
    def __init__(self):
        self.animation_count = 0

    def animate_latest_move(self):
        self.animation_count += 1


class BotGameplayTests(unittest.TestCase):
    def setUp(self):
        self.game = ChessGame.__new__(ChessGame)
        self.game.gamemode = ChessGame.BOT_MODE
        self.game.bot_difficulty = 'easy'
        self.game.bot = EasyBot(rng=random.Random(7))
        self.game.game_state = GameState()
        self.game.move_animation = AnimationStub()
        self.game.input_handler = InputStub()

    def test_player_starts_as_white(self):
        self.assertTrue(self.game.game_state.white_to_move)
        self.assertFalse(self.game.is_bot_turn)

    def test_easy_bot_plays_black_after_white_move(self):
        outcome = self.game.game_state.move.handle_piece_move((6, 4), (4, 4))

        self.assertEqual(outcome, 'moved')
        self.assertTrue(self.game.is_bot_turn)
        self.assertTrue(self.game._play_bot_turn())
        self.assertTrue(self.game.game_state.white_to_move)
        self.assertEqual(len(self.game.game_state.move.notation), 2)
        self.assertEqual(self.game.input_handler.animation_count, 1)

    def test_bot_waits_for_player_animation(self):
        self.game.game_state.move.handle_piece_move((6, 4), (4, 4))
        self.game.move_animation.is_animating = True

        self.assertFalse(self.game._play_bot_turn())
        self.assertFalse(self.game.game_state.white_to_move)


if __name__ == '__main__':
    unittest.main()
