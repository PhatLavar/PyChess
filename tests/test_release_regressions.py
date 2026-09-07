import os
from pathlib import Path
import random
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

from chess_app.chess_game import ChessGame
from chess_app.input_handler import InputHandler
from chess_app.match_history import MatchHistory
from chess_engine import GameState
from chess_engine.bots import EasyBot, ImpossibleBot, MasterBot, MediumBot
from chess_engine.utilities import EMP
from chess_ui.animations import MoveAnimation
from chess_ui.renderers import GameRenderer


def sparse_state(pieces):
    state = GameState()
    state.board.board = [[EMP] * 8 for _ in range(8)]
    for square, piece in pieces:
        state.board.set_piece(square, piece)
        if piece == 'wK':
            state.white_king_position = square
        elif piece == 'bK':
            state.black_king_position = square
    state.castling_rights = {
        color: {'king_side': False, 'queen_side': False} for color in 'wb'
    }
    return state


class ReleaseRegressionTests(unittest.TestCase):
    def test_promotion_cancel_preserves_previous_bot_move(self):
        state = sparse_state([((7, 4), 'wK'), ((0, 4), 'bK'), ((1, 0), 'wP')])
        state.white_to_move = False
        state.move.handle_piece_move((0, 4), (1, 4))
        state.move.handle_piece_move((1, 0), (0, 0))
        self.assertTrue(state.promotion_pending)
        game = ChessGame.__new__(ChessGame)
        game.game_state = state
        game.gamemode = ChessGame.BOT_MODE
        game.bot = EasyBot()
        game.input_handler = InputHandler(state, MoveAnimation())

        self.assertTrue(game.handle_undo())
        self.assertFalse(state.promotion_pending)
        self.assertTrue(state.white_to_move)
        self.assertEqual(len(state.move.notation), 1)
        self.assertEqual(state.board.get_piece((1, 4)), 'bK')
        self.assertEqual(state.board.get_piece((1, 0)), 'wP')

    def test_zero_choice_window_selects_exact_best_score(self):
        state = GameState()
        state.move.handle_piece_move((6, 2), (4, 2))
        state.move.handle_piece_move((1, 4), (3, 4))
        bot = MediumBot(choice_window=0, rng=random.Random(0))
        chosen = bot.choose_move(state)
        exact_scores = {
            move: bot._minimax(bot._state_after_move(state, move), 1,
                               float('-inf'), float('inf'))
            for move in state.move.get_valid_moves()
        }
        self.assertEqual(exact_scores[chosen], max(exact_scores.values()))

    def test_quiescence_searches_quiet_evasions_without_stand_pat(self):
        state = sparse_state([
            ((7, 4), 'wK'), ((0, 0), 'bK'), ((0, 4), 'bR'), ((7, 7), 'wQ'),
        ])
        self.assertTrue(state.move_validator.in_check())
        moves = state.move.get_valid_moves()
        self.assertTrue(moves)
        for color in ('w', 'b'):
            with self.subTest(bot_color=color):
                bot = MasterBot()
                bot.color = color
                self.assertTrue(all(not bot._is_capture(state, move) for move in moves))
                # Make standing still artificially preferable to every evasion.
                stand_pat = 10000 if color == 'w' else -10000
                with patch.object(bot, '_evaluate', side_effect=lambda s: stand_pat if s is state else 0), patch.object(
                    bot, '_state_after_move', wraps=bot._state_after_move
                ) as expand:
                    result = bot._quiescence(state, float('-inf'), float('inf'), 1)
                self.assertEqual(expand.call_count, len(moves))
                self.assertEqual(result, 0)

    def test_saved_history_retains_moves_and_consecutive_undos(self):
        state = GameState()
        state.move.handle_piece_move((6, 4), (4, 4))
        state.move.handle_piece_move((1, 4), (3, 4))
        state.move.handle_piece_move((7, 6), (5, 5))
        state.move.handle_undo_move()
        state.move.handle_undo_move()
        expected = [
            '[MOVE] wP e2->e4', '[MOVE] bP e7->e5', '[MOVE] wN g1->f3',
            '[UNDO] wN f3->g1', '[UNDO] bP e5->e7',
        ]
        self.assertEqual(state.move.move_log, expected)
        self.assertEqual(len(state.move.notation), 1)
        with TemporaryDirectory() as directory:
            path = MatchHistory(directory).save(state.move.move_log, 'player')
            self.assertEqual(path.read_text().splitlines(), expected)

    def test_bundled_assets_resolve_from_another_working_directory(self):
        original_directory = Path.cwd()
        project_root = Path(__file__).resolve().parent.parent
        with TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                renderer = GameRenderer(GameState(), Mock(), Mock(), Mock())
                self.assertEqual(len(renderer.load_piece_images()), 12)
                bundled = project_root / 'assets' / 'stockfish' / 'stockfish.exe'
                with patch('chess_engine.bots.impossible_bot.shutil.which', return_value=None), patch.dict(
                    os.environ, {'PYCHESS_STOCKFISH_PATH': ''}
                ), patch.object(Path, 'is_file', autospec=True, side_effect=lambda p: p == bundled):
                    self.assertEqual(ImpossibleBot().executable_path, bundled.resolve())
            finally:
                os.chdir(original_directory)


if __name__ == '__main__':
    unittest.main()
