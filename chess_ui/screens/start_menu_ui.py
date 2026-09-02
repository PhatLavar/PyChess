import pygame as pg

from chess_ui.config import (
    BOARD_DARK_COLOR,
    BOARD_DIMENSION,
    BOARD_LIGHT_COLOR,
    BOARD_PIXEL_SIZE,
    BUTTON_BORDER_WIDTH,
    BUTTON_CORNER_RADIUS,
    BUTTON_DEFAULT_COLOR,
    BUTTON_FONT_SIZE,
    BUTTON_HOVER_COLOR,
    BUTTON_SELECTED_BORDER_COLOR,
    BUTTON_SELECTED_COLOR,
    MODAL_OVERLAY_ALPHA,
    MODAL_OVERLAY_COLOR,
    SQUARE_SIZE,
    TEXT_COLOR,
    TITLE_FONT_SIZE,
)


class StartMenuUI:
    """
    Display the initial matchup selection and bot difficulties.
    """
    MODE_VIEW = 'mode'
    DIFFICULTY_VIEW = 'difficulty'

    BUTTON_GAP = 10
    MODE_TITLE_TO_BUTTON_GAP = 38
    DIFFICULTY_ROW_GAP = 12
    TITLE_TO_DIFFICULTIES_GAP = 24
    ACTIONS_TOP_GAP = 22
    MODE_BUTTON_HEIGHT = 52
    DIFFICULTY_BUTTON_HEIGHT = 48
    ACTION_BUTTON_HEIGHT = 50
    ACTION_BACK_WIDTH_RATIO = 0.30
    DIFFICULTY_PANEL_WIDTH = 390

    def __init__(self):
        self.active_view = self.MODE_VIEW
        self.pending_difficulty = 'easy'
        self.pending_bot_mode = None
        self.title_font = pg.font.Font(None, 84)
        self.difficulty_title_font = pg.font.Font(None, TITLE_FONT_SIZE)
        self.button_font = pg.font.Font(None, BUTTON_FONT_SIZE)
        self._create_mode_layout()
        self._create_difficulty_layout()

    ####################################################################################
    # ---------------------------------- LAYOUTING -------------------------------------
    ####################################################################################

    def _create_mode_layout(self):
        """
        Stack three full-width matchup buttons under the PyChess title.
        """
        title_width, title_height = self.title_font.size('PyChess')
        group_height = (
            title_height
            + self.MODE_TITLE_TO_BUTTON_GAP
            + self.MODE_BUTTON_HEIGHT * 3
            + self.BUTTON_GAP * 2
        )
        group_top = BOARD_PIXEL_SIZE // 2 - group_height // 2
        self.mode_title_center_y = group_top + title_height // 2
        button_y = (
            group_top
            + title_height
            + self.MODE_TITLE_TO_BUTTON_GAP
        )
        row_x = BOARD_PIXEL_SIZE // 2 - title_width // 2

        self.player_bot_button = pg.Rect(
            row_x,
            button_y,
            title_width,
            self.MODE_BUTTON_HEIGHT,
        )
        self.player_player_button = pg.Rect(
            row_x,
            self.player_bot_button.bottom + self.BUTTON_GAP,
            title_width,
            self.MODE_BUTTON_HEIGHT,
        )
        self.bot_bot_button = pg.Rect(
            row_x,
            self.player_player_button.bottom + self.BUTTON_GAP,
            title_width,
            self.MODE_BUTTON_HEIGHT,
        )

    def _create_difficulty_layout(self):
        """
        Create two difficulty rows and a 30/70 action row.
        """
        _, title_height = self.difficulty_title_font.size('Difficulty')
        group_height = (
            title_height
            + self.TITLE_TO_DIFFICULTIES_GAP
            + self.DIFFICULTY_BUTTON_HEIGHT * 2
            + self.DIFFICULTY_ROW_GAP
            + self.ACTIONS_TOP_GAP
            + self.ACTION_BUTTON_HEIGHT
        )
        group_top = BOARD_PIXEL_SIZE // 2 - group_height // 2
        self.difficulty_title_center_y = group_top + title_height // 2
        panel_x = (
            BOARD_PIXEL_SIZE // 2 - self.DIFFICULTY_PANEL_WIDTH // 2
        )
        first_row_y = (
            group_top
            + title_height
            + self.TITLE_TO_DIFFICULTIES_GAP
        )

        first_width = self.DIFFICULTY_PANEL_WIDTH - self.BUTTON_GAP * 2
        easy_width = int(first_width * 0.30)
        medium_width = int(first_width * 0.40)
        hard_width = first_width - easy_width - medium_width

        self.easy_button = pg.Rect(
            panel_x,
            first_row_y,
            easy_width,
            self.DIFFICULTY_BUTTON_HEIGHT,
        )
        self.medium_button = pg.Rect(
            self.easy_button.right + self.BUTTON_GAP,
            first_row_y,
            medium_width,
            self.DIFFICULTY_BUTTON_HEIGHT,
        )
        self.hard_button = pg.Rect(
            self.medium_button.right + self.BUTTON_GAP,
            first_row_y,
            hard_width,
            self.DIFFICULTY_BUTTON_HEIGHT,
        )

        second_row_y = self.easy_button.bottom + self.DIFFICULTY_ROW_GAP
        second_width = self.DIFFICULTY_PANEL_WIDTH - self.BUTTON_GAP
        master_width = int(second_width * 0.50)
        impossible_width = second_width - master_width

        self.master_button = pg.Rect(
            panel_x,
            second_row_y,
            master_width,
            self.DIFFICULTY_BUTTON_HEIGHT,
        )
        self.impossible_button = pg.Rect(
            self.master_button.right + self.BUTTON_GAP,
            second_row_y,
            impossible_width,
            self.DIFFICULTY_BUTTON_HEIGHT,
        )

        action_width = self.DIFFICULTY_PANEL_WIDTH - self.BUTTON_GAP
        back_width = int(action_width * self.ACTION_BACK_WIDTH_RATIO)
        select_width = action_width - back_width
        actions_y = self.master_button.bottom + self.ACTIONS_TOP_GAP
        self.back_button = pg.Rect(
            panel_x,
            actions_y,
            back_width,
            self.ACTION_BUTTON_HEIGHT,
        )
        self.select_difficulty_button = pg.Rect(
            self.back_button.right + self.BUTTON_GAP,
            actions_y,
            select_width,
            self.ACTION_BUTTON_HEIGHT,
        )
        self.difficulty_buttons = (
            ('Easy', 'easy', self.easy_button),
            ('Medium', 'medium', self.medium_button),
            ('Hard', 'hard', self.hard_button),
            ('Master', 'master', self.master_button),
            ('Impossible', 'impossible', self.impossible_button),
        )

    ####################################################################################
    # ---------------------------------- RENDERING -------------------------------------
    ####################################################################################

    def draw(self, screen):
        """
        Draw an empty chessboard, dark overlay, and active menu.
        """
        self._draw_empty_board(screen)
        self._draw_dark_overlay(screen)

        if self.active_view == self.DIFFICULTY_VIEW:
            self._draw_difficulty_view(screen)
        else:
            self._draw_mode_view(screen)

    def _draw_empty_board(self, screen):
        """Draw the normal chessboard without pieces."""
        colors = (
            pg.Color(BOARD_LIGHT_COLOR),
            pg.Color(BOARD_DARK_COLOR),
        )
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                square = pg.Rect(
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                )
                pg.draw.rect(screen, colors[(row + col) % 2], square)

    def _draw_dark_overlay(self, screen):
        """
        Darken the empty board like the game-over modal.
        """
        overlay = pg.Surface(
            (BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE),
            pg.SRCALPHA,
        )
        overlay.fill((*MODAL_OVERLAY_COLOR, MODAL_OVERLAY_ALPHA))
        screen.blit(overlay, (0, 0))

    def _draw_mode_view(self, screen):
        """
        Draw PyChess with the three available matchups.
        """
        title = self.title_font.render('PyChess', True, pg.Color(TEXT_COLOR))
        title_rect = title.get_rect(
            center=(BOARD_PIXEL_SIZE // 2, self.mode_title_center_y)
        )
        screen.blit(title, title_rect)
        self._draw_button(screen, self.player_bot_button, 'Player - Bot')
        self._draw_button(screen, self.player_player_button, 'Player - Player')
        self._draw_button(screen, self.bot_bot_button, 'Bot - Bot')

    def _draw_difficulty_view(self, screen):
        """
        Draw the difficulty title and requested button rows.
        """
        title = self.difficulty_title_font.render(
            'Difficulty',
            True,
            pg.Color(TEXT_COLOR),
        )
        title_rect = title.get_rect(
            center=(
                BOARD_PIXEL_SIZE // 2,
                self.difficulty_title_center_y,
            )
        )
        screen.blit(title, title_rect)

        for label, difficulty, button in self.difficulty_buttons:
            self._draw_button(
                screen,
                button,
                label,
                selected=difficulty == self.pending_difficulty,
            )
        self._draw_button(screen, self.back_button, 'Back')
        self._draw_button(
            screen,
            self.select_difficulty_button,
            'Select Difficulty',
        )

    def _draw_button(self, screen, button, label, selected=False):
        """
        Draw one menu button with hover feedback.
        """
        if selected:
            color = BUTTON_SELECTED_COLOR
            border_color = BUTTON_SELECTED_BORDER_COLOR
        elif button.collidepoint(pg.mouse.get_pos()):
            color = BUTTON_HOVER_COLOR
            border_color = TEXT_COLOR
        else:
            color = BUTTON_DEFAULT_COLOR
            border_color = TEXT_COLOR
        pg.draw.rect(
            screen,
            pg.Color(color),
            button,
            border_radius=BUTTON_CORNER_RADIUS,
        )
        pg.draw.rect(
            screen,
            pg.Color(border_color),
            button,
            width=BUTTON_BORDER_WIDTH,
            border_radius=BUTTON_CORNER_RADIUS,
        )
        text = self.button_font.render(label, True, pg.Color(TEXT_COLOR))
        screen.blit(text, text.get_rect(center=button.center))

    ####################################################################################
    # -------------------------------- INTERACTION -------------------------------------
    ####################################################################################

    def handle_click(self, mouse_position):
        """
        Return a selected game mode or bot difficulty.
        """
        if self.active_view == self.MODE_VIEW:
            return self._handle_mode_click(mouse_position)
        return self._handle_difficulty_click(mouse_position)

    def _handle_mode_click(self, mouse_position):
        """
        Handle matchup clicks.
        """
        if self.player_player_button.collidepoint(mouse_position):
            return 'player'
        if self.player_bot_button.collidepoint(mouse_position):
            self.pending_bot_mode = 'bot'
            self.pending_difficulty = 'easy'
            self.active_view = self.DIFFICULTY_VIEW
        elif self.bot_bot_button.collidepoint(mouse_position):
            self.pending_bot_mode = 'bot_bot'
            self.pending_difficulty = 'easy'
            self.active_view = self.DIFFICULTY_VIEW
        return None

    def _handle_difficulty_click(self, mouse_position):
        """
        Handle difficulty and Back clicks.
        """
        for _, difficulty, button in self.difficulty_buttons:
            if button.collidepoint(mouse_position):
                self.pending_difficulty = difficulty
                return None
        if self.back_button.collidepoint(mouse_position):
            self.pending_difficulty = 'easy'
            self.pending_bot_mode = None
            self.active_view = self.MODE_VIEW
            return None
        if self.select_difficulty_button.collidepoint(mouse_position):
            return self.pending_bot_mode, self.pending_difficulty
        return None
