import pygame as pg


class EventHandler:
    """
    Route Pygame events to application, UI, or chess input handlers.
    """

    def __init__(self, chess_game):
        """
        Bind event routing to the running application.
        """
        self.chess_game = chess_game

    def process_events(self):
        """
        Process one frame of events and report whether to keep running.

        Returns:
            'False' after a window-close event; otherwise 'True'.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.chess_game.terminate_match()
                return False

            if self.chess_game.active_screen == self.chess_game.START_SCREEN:
                if event.type == pg.MOUSEBUTTONDOWN:
                    self._handle_start_menu_click(event.pos)
                continue

            if event.type == pg.MOUSEMOTION:
                self.chess_game.input_handler.handle_mouse_motion(event.pos)

            elif event.type == pg.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos)

            elif event.type == pg.KEYDOWN and event.key == pg.K_z:
                self.chess_game.handle_undo()

        return True

    def _handle_mouse_click(self, mouse_position):
        """
        Route clicks to the active modal or the chessboard.
        """
        game_state = self.chess_game.game_state

        if game_state.game_over:
            action = self.chess_game.game_over_ui.handle_click(mouse_position)
            self._handle_game_over_action(action)
            return

        if self.chess_game.is_bot_turn:
            self.chess_game.input_handler.reset_selection()
            return

        state_changed = self.chess_game.input_handler.handle_mouse_click(
            mouse_position
        )

        if state_changed and game_state.game_over:
            self.chess_game.game_over_ui.activate()

    def _handle_start_menu_click(self, mouse_position):
        """
        Apply an action returned by the start menu.
        """
        action = self.chess_game.start_menu_ui.handle_click(
            mouse_position
        )

        if action == 'player':
            self.chess_game.start_player_game()
            return

        if isinstance(action, tuple) and action[0] == 'bot':
            self.chess_game.start_bot_game(action[1])

    def _handle_game_over_action(self, action):
        """
        Apply a game-over UI action when one was returned.
        """
        if action == 'rematch':
            self.chess_game.rematch()
            return

        if isinstance(action, tuple) and action[0] == 'change_mode':
            self.chess_game.change_gamemode(action[1])
