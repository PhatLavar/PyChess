import unittest
from datetime import datetime
from tempfile import TemporaryDirectory
from unittest.mock import Mock

from chess_app.chess_game import ChessGame
from chess_app.match_history import MatchHistory
from chess_engine import GameState


class MatchHistorySavingTests(unittest.TestCase):
    def setUp(self):
        self.game = ChessGame.__new__(ChessGame)
        self.game.game_state = GameState()
        self.game.match_history = Mock()
        self.game.match_history_saved = False
        self.game.gamemode = ChessGame.PLAYER_MODE
        self.game.bot = None
        self.game.white_bot = None

    def test_terminating_fresh_match_does_not_save(self):
        result = self.game.terminate_match()

        self.assertIsNone(result)
        self.game.match_history.save.assert_not_called()
        self.assertEqual(self.game.game_state.move.move_log, [])

    def test_terminating_after_all_moves_are_undone_does_not_save(self):
        self.game.game_state.move.handle_piece_move((6, 4), (4, 4))
        self.game.game_state.move.handle_undo_move()

        result = self.game.terminate_match()

        self.assertIsNone(result)
        self.game.match_history.save.assert_not_called()

    def test_terminating_match_with_an_applied_move_saves(self):
        expected_path = object()
        self.game.match_history.save.return_value = expected_path
        self.game.game_state.move.handle_piece_move((6, 4), (4, 4))

        result = self.game.terminate_match()

        self.assertIs(result, expected_path)
        self.game.match_history.save.assert_called_once_with(
            self.game.game_state.move.move_log,
            ChessGame.PLAYER_MODE,
        )
        self.assertEqual(
            self.game.game_state.move.move_log[-1],
            '[ENDMATCH] TERMINATED',
        )

    def test_completed_initial_position_does_not_save(self):
        self.game.game_state.game_over = True

        result = self.game._save_completed_match()

        self.assertIsNone(result)
        self.game.match_history.save.assert_not_called()

    def test_each_gamemode_saves_in_its_own_folder(self):
        expected_folders = {
            ChessGame.PLAYER_MODE: 'player-player',
            ChessGame.BOT_MODE: 'player-bot',
            ChessGame.BOT_BOT_MODE: 'bot-bot',
        }

        with TemporaryDirectory() as temporary_directory:
            history = MatchHistory(temporary_directory)

            for gamemode, folder_name in expected_folders.items():
                path = history.save(
                    ['[MOVE] test'],
                    gamemode,
                    completed_at=datetime(2026, 9, 3, 12, 34),
                )

                self.assertEqual(path.parent.name, folder_name)
                self.assertEqual(path.name, '20260903-1234.txt')
                self.assertEqual(path.read_text(encoding='utf-8'), '[MOVE] test\n')

    def test_ensure_directory_creates_all_mode_folders(self):
        with TemporaryDirectory() as temporary_directory:
            history = MatchHistory(temporary_directory)
            history.ensure_directory()

            for folder_name in MatchHistory.MODE_FOLDERS.values():
                self.assertTrue(
                    (history.history_directory / folder_name).is_dir()
                )


if __name__ == '__main__':
    unittest.main()
