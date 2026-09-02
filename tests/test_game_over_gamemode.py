import unittest
from types import SimpleNamespace
from unittest.mock import patch

import pygame as pg

from chess_ui.config import GAME_OVER_DELAY_MS
from chess_ui.screens.game_over_ui import GameOverUI


class GameOverGamemodeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pg.init()

    @classmethod
    def tearDownClass(cls):
        pg.quit()

    def setUp(self):
        state = SimpleNamespace(game_over=True)
        self.ui = GameOverUI(state, 'player')
        self.ui.started_at = 0
        self.elapsed_patch = patch.object(
            self.ui,
            'get_elapsed_time',
            return_value=GAME_OVER_DELAY_MS,
        )
        self.elapsed_patch.start()
        self.ui.handle_click(self.ui.change_mode_button.center)

    def tearDown(self):
        self.elapsed_patch.stop()

    def _mode_button(self, action):
        return next(
            button
            for _, button_action, button in self.ui.gamemode_buttons
            if button_action == action
        )

    def test_player_player_starts_immediately(self):
        action = self.ui.handle_click(self._mode_button('player').center)

        self.assertEqual(action, 'player')

    def test_player_bot_opens_difficulty_and_returns_selection(self):
        action = self.ui.handle_click(self._mode_button('bot').center)

        self.assertIsNone(action)
        self.assertEqual(self.ui.active_view, self.ui.DIFFICULTY_VIEW)

        self.ui.handle_click(self.ui.difficulty_menu.hard_button.center)
        action = self.ui.handle_click(
            self.ui.difficulty_menu.select_difficulty_button.center
        )

        self.assertEqual(action, ('bot', 'hard'))

    def test_bot_bot_opens_difficulty_and_returns_selection(self):
        self.ui.handle_click(self._mode_button('bot_bot').center)
        self.ui.handle_click(self.ui.difficulty_menu.medium_button.center)
        action = self.ui.handle_click(
            self.ui.difficulty_menu.select_difficulty_button.center
        )

        self.assertEqual(action, ('bot_bot', 'medium'))

    def test_difficulty_back_returns_to_gamemode_choices(self):
        self.ui.handle_click(self._mode_button('bot_bot').center)
        action = self.ui.handle_click(self.ui.difficulty_menu.back_button.center)

        self.assertIsNone(action)
        self.assertEqual(self.ui.active_view, self.ui.GAMEMODE_VIEW)


if __name__ == '__main__':
    unittest.main()
