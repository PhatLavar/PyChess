import pygame as pg


class EventHandler:
    """Route Pygame events to application, UI, or chess input handlers."""

    def __init__(self, chess_game):
        """Bind event routing to the running application."""
        self.chess_game = chess_game

    def process_events(self):
        """Process one frame of events and report whether to keep running.

        Returns:
            ``False`` after a window-close event; otherwise ``True``.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            if event.type == pg.MOUSEMOTION:
                self.chess_game.input_handler.handle_mouse_motion(event.pos)

            elif event.type == pg.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos)

            elif event.type == pg.KEYDOWN and event.key == pg.K_z:
                self.chess_game.input_handler.handle_undo()

        return True

    def _handle_mouse_click(self, mouse_position):
        """Route clicks to the active modal or the chessboard."""
        game_state = self.chess_game.game_state

        if game_state.game_over:
            action = self.chess_game.game_over_ui.handle_click(mouse_position)
            self._handle_game_over_action(action)
            return

        state_changed = self.chess_game.input_handler.handle_mouse_click(
            mouse_position
        )

        if state_changed and game_state.game_over:
            self.chess_game.game_over_ui.activate()

    def _handle_game_over_action(self, action):
        """Apply a game-over UI action when one was returned."""
        if action == 'rematch':
            self.chess_game.rematch()
            return

        if isinstance(action, tuple) and action[0] == 'change_mode':
            self.chess_game.change_gamemode(action[1])
