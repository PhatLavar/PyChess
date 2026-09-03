import math
import pygame as pg

from chess_ui.screens.start_menu_ui import StartMenuUI

from chess_ui.config import (
    BOARD_PIXEL_SIZE,
    BUTTON_DEFAULT_COLOR,
    BUTTON_BORDER_WIDTH,
    BUTTON_CORNER_RADIUS,
    BUTTON_FONT_SIZE,
    BUTTON_HOVER_COLOR,
    BUTTON_SELECTED_BORDER_COLOR,
    BUTTON_SELECTED_COLOR,
    ENDGAME_FLASH_CYCLE_MS,
    ENDGAME_SQUARE_COLOR,
    ENDGAME_SQUARE_MAX_OPACITY,
    ENDGAME_TEXT_COLOR,
    ENDGAME_TEXT_MAX_OPACITY,
    ENDGAME_TEXT_MIN_OPACITY,
    FULL_ALPHA,
    GAME_OVER_DELAY_MS,
    GAMEMODE_ACTIONS_TOP_GAP,
    GAMEMODE_ACTION_HEIGHT,
    GAMEMODE_BUTTON_GAP,
    GAMEMODE_BUTTON_HEIGHT,
    GAMEMODE_PANEL_WIDTH,
    GAMEMODE_TITLE_GAP,
    MODAL_OVERLAY_ALPHA,
    MODAL_OVERLAY_COLOR,
    RESULT_BUTTON_GAP,
    RESULT_BUTTON_HEIGHT,
    RESULT_BUTTON_WIDTH,
    RESULT_FONT_SIZE,
    RESULT_TO_BUTTON_GAP,
    SQUARE_SIZE,
    STATUS_FONT_SIZE,
    TEXT_COLOR,
    TEXT_SHADOW_COLOR,
    TEXT_SHADOW_OFFSET,
    TITLE_FONT_SIZE,
)


class GameOverUI:
    """
    Render terminal-match animation, results, and gamemode selection.
    """

    RESULT_VIEW = 'result'
    GAMEMODE_VIEW = 'gamemode'
    DIFFICULTY_VIEW = 'difficulty'
    GAMEMODE_OPTIONS = (
        ('Player - Bot', 'bot'),
        ('Player - Player', 'player'),
        ('Bot - Bot', 'bot_bot'),
    )

    def __init__(self, game_state, current_gamemode):
        """
        Create inactive terminal UI for a match.

        Args:
            game_state: Engine state whose result will be displayed.
            current_gamemode: Confirmed application gamemode shown initially.
        """
        self.game_state = game_state
        self.current_gamemode = current_gamemode
        self.active_view = self.RESULT_VIEW
        self.started_at = None
        self.difficulty_menu = StartMenuUI()

        self.status_font = pg.font.Font(None, STATUS_FONT_SIZE)
        self.result_font = pg.font.Font(None, RESULT_FONT_SIZE)
        self.title_font = pg.font.Font(None, TITLE_FONT_SIZE)
        self.button_font = pg.font.Font(None, BUTTON_FONT_SIZE)

        self._create_result_layout()
        self._create_gamemode_layout()

    ####################################################################################
    # --------------------------------- LIFE CYCLE -------------------------------------
    ####################################################################################

    def activate(self):
        """
        Start the terminal flash timer and return its Pygame timestamp.
        """
        if self.started_at is None:
            self.started_at = pg.time.get_ticks()
        return self.started_at

    def get_elapsed_time(self):
        """
        Return milliseconds since activation, or zero before activation.
        """
        if self.started_at is None:
            return 0
        return pg.time.get_ticks() - self.started_at

    ####################################################################################
    # ---------------------------------- LAYOUTS ---------------------------------------
    ####################################################################################

    def _create_result_layout(self):
        """
        Calculate one centered group for result text and action buttons.
        """
        center_x = BOARD_PIXEL_SIZE // 2
        center_y = BOARD_PIXEL_SIZE // 2
        result_height = self.result_font.get_linesize()
        group_height = (
            result_height
            + RESULT_TO_BUTTON_GAP
            + RESULT_BUTTON_HEIGHT * 2
            + RESULT_BUTTON_GAP
        )
        group_top = center_y - group_height // 2

        self.result_center_y = group_top + result_height // 2
        rematch_y = group_top + result_height + RESULT_TO_BUTTON_GAP
        button_x = center_x - RESULT_BUTTON_WIDTH // 2

        self.rematch_button = pg.Rect(
            button_x,
            rematch_y,
            RESULT_BUTTON_WIDTH,
            RESULT_BUTTON_HEIGHT,
        )
        self.change_mode_button = pg.Rect(
            button_x,
            self.rematch_button.bottom + RESULT_BUTTON_GAP,
            RESULT_BUTTON_WIDTH,
            RESULT_BUTTON_HEIGHT,
        )

    def _create_gamemode_layout(self):
        """
        Calculate centered mode choices and 30/70 action buttons.
        """
        center_x = BOARD_PIXEL_SIZE // 2
        title_height = self.title_font.get_linesize()
        modes_height = GAMEMODE_BUTTON_HEIGHT * len(self.GAMEMODE_OPTIONS)
        mode_gaps_height = GAMEMODE_BUTTON_GAP * (
            len(self.GAMEMODE_OPTIONS) - 1
        )
        group_height = (
            title_height
            + GAMEMODE_TITLE_GAP
            + modes_height
            + mode_gaps_height
            + GAMEMODE_ACTIONS_TOP_GAP
            + GAMEMODE_ACTION_HEIGHT
        )
        group_top = BOARD_PIXEL_SIZE // 2 - group_height // 2
        self.gamemode_title_center_y = group_top + title_height // 2
        modes_top = group_top + title_height + GAMEMODE_TITLE_GAP

        self.gamemode_buttons = []
        for index, option in enumerate(self.GAMEMODE_OPTIONS):
            label, action = option
            button_rect = pg.Rect(
                center_x - GAMEMODE_PANEL_WIDTH // 2,
                modes_top + index * (
                    GAMEMODE_BUTTON_HEIGHT + GAMEMODE_BUTTON_GAP
                ),
                GAMEMODE_PANEL_WIDTH,
                GAMEMODE_BUTTON_HEIGHT,
            )
            self.gamemode_buttons.append((label, action, button_rect))

        actions_y = self.gamemode_buttons[-1][2].bottom + GAMEMODE_ACTIONS_TOP_GAP
        actions_x = center_x - GAMEMODE_PANEL_WIDTH // 2

        self.back_button = pg.Rect(
            actions_x,
            actions_y,
            GAMEMODE_PANEL_WIDTH,
            GAMEMODE_ACTION_HEIGHT,
        )

    ####################################################################################
    # --------------------------------- RENDERING --------------------------------------
    ####################################################################################

    def draw(self, screen):
        """
        Draw the active terminal phase; draw nothing before game over.
        """
        if not self.game_state.game_over:
            return

        self.activate()
        elapsed = self.get_elapsed_time()

        if elapsed < GAME_OVER_DELAY_MS:
            self._draw_flashing_phase(screen, elapsed)
        elif self.active_view == self.DIFFICULTY_VIEW:
            self._draw_dark_overlay(screen)
            self.difficulty_menu._draw_difficulty_view(screen)
        elif self.active_view == self.GAMEMODE_VIEW:
            self._draw_gamemode_screen(screen)
        else:
            self._draw_result_screen(screen)

    def _draw_flashing_phase(self, screen, elapsed):
        """
        Draw synchronized terminal-square and status-text pulses.
        """
        pulse = self._get_flash_pulse(elapsed)
        self._draw_flashing_king_square(screen, pulse)
        self._draw_status_text(screen, pulse)

    def _get_flash_pulse(self, elapsed):
        """
        Return a smooth repeating value from zero to one.
        """
        phase = (elapsed % ENDGAME_FLASH_CYCLE_MS) / ENDGAME_FLASH_CYCLE_MS
        return (math.sin(phase * math.tau - math.pi / 2) + 1) / 2

    def _draw_flashing_king_square(self, screen, pulse):
        """
        Pulse a red overlay on the terminal side-to-move king square.
        """
        row, col = self.game_state.get_terminal_king_square()
        max_alpha = int(FULL_ALPHA * ENDGAME_SQUARE_MAX_OPACITY)
        overlay = pg.Surface((SQUARE_SIZE, SQUARE_SIZE), pg.SRCALPHA)
        overlay.fill((*ENDGAME_SQUARE_COLOR, int(pulse * max_alpha)))
        screen.blit(overlay, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def _draw_status_text(self, screen, pulse):
        """
        Pulse the terminal-status text in the board center.
        """
        messages = {
            'checkmate': ('CHECKMATE!',),
            'stalemate': ('STALEMATE!',),
            'repetition': ('THREEFOLD', 'REPETITION!'),
        }
        opacity_range = ENDGAME_TEXT_MAX_OPACITY - ENDGAME_TEXT_MIN_OPACITY
        opacity = ENDGAME_TEXT_MIN_OPACITY + pulse * opacity_range
        alpha = int(opacity * FULL_ALPHA)
        lines = messages[self.game_state.game_result]
        line_height = self.status_font.get_linesize()
        first_center_y = (
            BOARD_PIXEL_SIZE // 2
            - (len(lines) - 1) * line_height // 2
        )

        for index, message in enumerate(lines):
            text = self.status_font.render(
                message,
                True,
                pg.Color(ENDGAME_TEXT_COLOR),
            )
            shadow = self.status_font.render(
                message,
                True,
                pg.Color(TEXT_SHADOW_COLOR),
            )
            text.set_alpha(alpha)
            shadow.set_alpha(alpha)
            text_rect = text.get_rect(
                center=(
                    BOARD_PIXEL_SIZE // 2,
                    first_center_y + index * line_height,
                )
            )
            screen.blit(
                shadow,
                text_rect.move(TEXT_SHADOW_OFFSET, TEXT_SHADOW_OFFSET),
            )
            screen.blit(text, text_rect)

    def _draw_result_screen(self, screen):
        """
        Draw the match result and result-screen actions.
        """
        self._draw_dark_overlay(screen)
        result = self.result_font.render(
            self._get_result_text(),
            True,
            pg.Color(TEXT_COLOR),
        )
        result_rect = result.get_rect(
            center=(BOARD_PIXEL_SIZE // 2, self.result_center_y)
        )
        screen.blit(result, result_rect)
        self._draw_button(screen, self.rematch_button, 'Rematch')
        self._draw_button(screen, self.change_mode_button, 'Change Gamemode')

    def _draw_gamemode_screen(self, screen):
        """
        Draw the three matchup choices and Back action.
        """
        self._draw_dark_overlay(screen)
        title = self.title_font.render('Select Gamemode', True, pg.Color(TEXT_COLOR))
        title_rect = title.get_rect(
            center=(BOARD_PIXEL_SIZE // 2, self.gamemode_title_center_y)
        )
        screen.blit(title, title_rect)

        for label, _, button_rect in self.gamemode_buttons:
            self._draw_button(screen, button_rect, label)

        self._draw_button(screen, self.back_button, 'Back')

    def _draw_dark_overlay(self, screen):
        """
        Darken the finished board behind the active modal.
        """
        overlay = pg.Surface(
            (BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE),
            pg.SRCALPHA,
        )
        overlay.fill((*MODAL_OVERLAY_COLOR, MODAL_OVERLAY_ALPHA))
        screen.blit(overlay, (0, 0))

    def _get_result_text(self):
        """
        Return `DRAW!` or the engine's winning-color message.
        """
        if self.game_state.game_result in ('stalemate', 'repetition'):
            return 'DRAW!'
        return self.game_state.winner

    def _draw_button(self, screen, button_rect, label, selected=False):
        """
        Draw one button with hover and pending-selection feedback.
        """
        is_hovered = button_rect.collidepoint(pg.mouse.get_pos())

        if selected:
            button_color = pg.Color(BUTTON_SELECTED_COLOR)
            border_color = pg.Color(BUTTON_SELECTED_BORDER_COLOR)
        elif is_hovered:
            button_color = pg.Color(BUTTON_HOVER_COLOR)
            border_color = pg.Color(TEXT_COLOR)
        else:
            button_color = pg.Color(BUTTON_DEFAULT_COLOR)
            border_color = pg.Color(TEXT_COLOR)

        pg.draw.rect(
            screen,
            button_color,
            button_rect,
            border_radius=BUTTON_CORNER_RADIUS,
        )
        pg.draw.rect(
            screen,
            border_color,
            button_rect,
            width=BUTTON_BORDER_WIDTH,
            border_radius=BUTTON_CORNER_RADIUS,
        )
        text = self.button_font.render(label, True, pg.Color(TEXT_COLOR))
        screen.blit(text, text.get_rect(center=button_rect.center))

    ####################################################################################
    # -------------------------------- INTERACTION -------------------------------------
    ####################################################################################

    def handle_click(self, mouse_position):
        """
        Handle a terminal-screen click.

        Returns:
            'rematch' for the Rematch button,
            'player' for Player-Player,
            ('bot', difficulty) for Player-Bot,
            ('bot_bot', difficulty) for Bot-Bot,
            or None when no application action is required.
        """
        if not self.game_state.game_over:
            return None

        if self.get_elapsed_time() < GAME_OVER_DELAY_MS:
            return None

        if self.active_view == self.GAMEMODE_VIEW:
            return self._handle_gamemode_click(mouse_position)

        if self.active_view == self.DIFFICULTY_VIEW:
            action = self.difficulty_menu.handle_click(mouse_position)
            if self.difficulty_menu.active_view == self.difficulty_menu.MODE_VIEW:
                self.active_view = self.GAMEMODE_VIEW
            return action

        if self.rematch_button.collidepoint(mouse_position):
            return 'rematch'

        if self.change_mode_button.collidepoint(mouse_position):
            self._reset_difficulty_menu()
            self.active_view = self.GAMEMODE_VIEW

        return None

    def _handle_gamemode_click(self, mouse_position):
        """
        Start Player-Player directly or open difficulty selection for bot modes.
        """
        for _, action, button_rect in self.gamemode_buttons:
            if button_rect.collidepoint(mouse_position):
                if action == 'player':
                    return action
                self.difficulty_menu.pending_bot_mode = action
                self.difficulty_menu.pending_difficulty = 'easy'
                self.difficulty_menu.active_view = (
                    self.difficulty_menu.DIFFICULTY_VIEW
                )
                self.active_view = self.DIFFICULTY_VIEW
                return None

        if self.back_button.collidepoint(mouse_position):
            self.active_view = self.RESULT_VIEW
            return None

        return None

    def _reset_difficulty_menu(self):
        """Reset shared difficulty-selection state for a fresh mode change."""
        self.difficulty_menu.active_view = self.difficulty_menu.MODE_VIEW
        self.difficulty_menu.pending_bot_mode = None
        self.difficulty_menu.pending_difficulty = 'easy'
