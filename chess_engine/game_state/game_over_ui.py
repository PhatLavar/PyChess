import math
import pygame as pg
from chess_engine.chess_properties import Board


class GameOverUI:
    FLASH_CYCLE = 1000

    def __init__(self, game_state):
        self.game_state = game_state

        self.status_font = pg.font.Font(None, 58)
        self.result_font = pg.font.Font(None, 48)
        self.title_font = pg.font.Font(None, 44)
        self.button_font = pg.font.Font(None, 30)

        self.active_view = 'result'
        self.pending_gamemode = self.game_state.gamemode

        button_width = 220
        button_height = 50
        result_button_gap = 28
        button_gap = 15
        center_x = Board.SCREEN_SIZE // 2
        center_y = Board.SCREEN_SIZE // 2

        result_height = self.result_font.get_linesize()
        group_height = (
            result_height
            + result_button_gap
            + button_height * 2
            + button_gap
        )
        group_top = center_y - group_height // 2

        self.result_center_y = group_top + result_height // 2
        rematch_y = group_top + result_height + result_button_gap

        self.rematch_button = pg.Rect(
            center_x - button_width // 2,
            rematch_y,
            button_width,
            button_height
        )

        self.change_mode_button = pg.Rect(
            center_x - button_width // 2,
            self.rematch_button.bottom + button_gap,
            button_width,
            button_height
        )

        self._create_gamemode_layout()

    def _create_gamemode_layout(self):
        center_x = Board.SCREEN_SIZE // 2
        panel_width = 300
        mode_height = 46
        mode_gap = 12
        action_height = 50
        action_gap = 10
        title_gap = 20
        actions_top_gap = 22
        title_height = self.title_font.get_linesize()

        group_height = (
            title_height
            + title_gap
            + mode_height * 3
            + mode_gap * 2
            + actions_top_gap
            + action_height
        )
        group_top = Board.SCREEN_SIZE // 2 - group_height // 2

        self.gamemode_title_center_y = group_top + title_height // 2
        modes_top = group_top + title_height + title_gap

        self.gamemode_buttons = []
        for index in range(3):
            rect = pg.Rect(
                center_x - panel_width // 2,
                modes_top + index * (mode_height + mode_gap),
                panel_width,
                mode_height
            )
            self.gamemode_buttons.append(
                (f'Gamemode {index + 1}', rect)
            )

        actions_y = self.gamemode_buttons[-1][1].bottom + actions_top_gap
        usable_width = panel_width - action_gap
        back_width = int(usable_width * 0.4)
        change_width = usable_width - back_width
        actions_x = center_x - panel_width // 2

        self.back_button = pg.Rect(
            actions_x,
            actions_y,
            back_width,
            action_height
        )
        self.confirm_change_button = pg.Rect(
            self.back_button.right + action_gap,
            actions_y,
            change_width,
            action_height
        )

    def draw(self, screen):
        if not self.game_state.game_over:
            return

        elapsed = self.game_state.get_game_over_elapsed()

        if elapsed < self.game_state.GAME_OVER_DELAY:
            self._draw_flashing_phase(screen, elapsed)
        elif self.active_view == 'gamemode':
            self._draw_gamemode_screen(screen)
        else:
            self._draw_result_screen(screen)

    def _draw_flashing_phase(self, screen, elapsed):
        pulse = self._get_flash_pulse(elapsed)
        self._draw_flashing_king_square(screen, pulse)
        self._draw_status_text(screen, pulse)

    def _get_flash_pulse(self, elapsed):
        phase = (elapsed % self.FLASH_CYCLE) / self.FLASH_CYCLE
        return (
            math.sin(phase * math.tau - math.pi / 2) + 1
        ) / 2

    def _draw_flashing_king_square(self, screen, pulse):
        king_square = self.game_state.get_losing_king_square()
        row, col = king_square

        max_alpha = int(255 * 0.75)
        alpha = int(pulse * max_alpha)

        square_overlay = pg.Surface(
            (Board.SQUARE_SIZE, Board.SQUARE_SIZE),
            pg.SRCALPHA
        )
        square_overlay.fill((255, 0, 0, alpha))

        screen.blit(
            square_overlay,
            (
                col * Board.SQUARE_SIZE,
                row * Board.SQUARE_SIZE
            )
        )

    def _draw_status_text(self, screen, pulse):
        if self.game_state.game_result == 'checkmate':
            message = 'CHECKMATE!'
        else:
            message = 'STALEMATE!'

        text = self.status_font.render(
            message,
            True,
            pg.Color('#FF4040')
        )

        shadow = self.status_font.render(
            message,
            True,
            pg.Color('black')
        )

        min_text_opacity = 0.15
        max_text_opacity = 0.90
        text_opacity = (
            min_text_opacity
            + pulse * (max_text_opacity - min_text_opacity)
        )
        text_alpha = int(text_opacity * 255)
        text.set_alpha(text_alpha)
        shadow.set_alpha(text_alpha)

        text_rect = text.get_rect(
            center=(
                Board.SCREEN_SIZE // 2,
                Board.SCREEN_SIZE // 2
            )
        )

        screen.blit(shadow, text_rect.move(3, 3))
        screen.blit(text, text_rect)

    def _draw_result_screen(self, screen):
        self._draw_dark_overlay(screen)

        result_text = self._get_result_text()
        text = self.result_font.render(
            result_text,
            True,
            pg.Color('White')
        )

        text_rect = text.get_rect(
            center=(
                Board.SCREEN_SIZE // 2,
                self.result_center_y
            )
        )
        screen.blit(text, text_rect)

        self._draw_button(
            screen,
            self.rematch_button,
            'Rematch'
        )

        self._draw_button(
            screen,
            self.change_mode_button,
            'Change Gamemode'
        )

    def _draw_gamemode_screen(self, screen):
        self._draw_dark_overlay(screen)

        title = self.title_font.render(
            'Select Gamemode',
            True,
            pg.Color('white')
        )
        screen.blit(
            title,
            title.get_rect(
                center=(
                    Board.SCREEN_SIZE // 2,
                    self.gamemode_title_center_y
                )
            )
        )

        for label, button_rect in self.gamemode_buttons:
            self._draw_button(
                screen,
                button_rect,
                label,
                selected=label == self.pending_gamemode
            )

        self._draw_button(screen, self.back_button, 'Back')
        self._draw_button(
            screen,
            self.confirm_change_button,
            'Select'
        )

    def _draw_dark_overlay(self, screen):
        overlay = pg.Surface(
            (Board.SCREEN_SIZE, Board.SCREEN_SIZE),
            pg.SRCALPHA
        )

        overlay.fill((10, 10, 10, 210))
        screen.blit(overlay, (0, 0))

    def _get_result_text(self):
        if self.game_state.game_result == 'stalemate':
            return 'DRAW!'
        return self.game_state.winner

    def _draw_button(self, screen, button_rect, label, selected=False):
        mouse_position = pg.mouse.get_pos()
        is_hovered = button_rect.collidepoint(mouse_position)

        if selected:
            button_color = pg.Color('#D49B2E')
        elif is_hovered:
            button_color = pg.Color("#51A57B")
        else:
            button_color = pg.Color("#26A867")

        pg.draw.rect(
            screen,
            button_color,
            button_rect,
            border_radius=8
        )

        border_color = (
            pg.Color('#FFE29A')
            if selected
            else pg.Color('white')
        )

        pg.draw.rect(
            screen,
            border_color,
            button_rect,
            width=2,
            border_radius=8
        )

        text = self.button_font.render(
            label,
            True,
            pg.Color('white')
        )

        screen.blit(
            text,
            text.get_rect(center=button_rect.center)
        )

    def handle_click(self, mouse_position):
        if not self.game_state.game_over:
            return None

        if (
            self.game_state.get_game_over_elapsed()
            < self.game_state.GAME_OVER_DELAY
        ):
            return None

        if self.active_view == 'gamemode':
            return self._handle_gamemode_click(mouse_position)

        if self.rematch_button.collidepoint(mouse_position):
            return 'rematch'

        if self.change_mode_button.collidepoint(mouse_position):
            self.pending_gamemode = self.game_state.gamemode
            self.active_view = 'gamemode'

        return None

    def _handle_gamemode_click(self, mouse_position):
        for label, button_rect in self.gamemode_buttons:
            if button_rect.collidepoint(mouse_position):
                self.pending_gamemode = label
                return None

        if self.back_button.collidepoint(mouse_position):
            self.pending_gamemode = self.game_state.gamemode
            self.active_view = 'result'
            return None

        if self.confirm_change_button.collidepoint(mouse_position):
            self.game_state.gamemode = self.pending_gamemode
            self.active_view = 'result'

        return None
