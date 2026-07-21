from chess_engine.helpers import EMP, piece_color, turn_color
from chess_engine.game_state.pawn_promotion_ui import PromotionUI


class InputHandler:
    def __init__(self, game_state):
        self.game_state = game_state
        self.promotion_ui = PromotionUI(game_state)

    @property
    def board(self):
        return self.game_state.board

    def handle_mouse_click(self, mouse_location):
        if self.game_state.promotion_pending:
            self.promotion_ui.handle_click(mouse_location)
            return

        square = self._get_square(mouse_location)
        piece = self.board.get_piece(square)

        if self._should_reset_selection(square, piece):
            self._reset_selection()
            return

        self._select_square(square)

        if len(self.game_state.player_clicked) == 2:
            self._execute_selected_move()

    def _get_square(self, mouse_location):
        col = mouse_location[0] // self.board.SQUARE_SIZE
        row = mouse_location[1] // self.board.SQUARE_SIZE
        return (row, col)

    def _should_reset_selection(self, square, piece):
        if square == self.game_state.selected_square:
            return True

        if len(self.game_state.player_clicked) != 0:
            return False

        return (
            piece == EMP
            or piece_color(piece) != turn_color(self.game_state.white_to_move)
        )

    def _reset_selection(self):
        self.game_state.selected_square = ()
        self.game_state.player_clicked = []

    def _select_square(self, square):
        self.game_state.selected_square = square
        self.game_state.player_clicked.append(square)

    def _execute_selected_move(self):
        self.game_state.moved_square = self.game_state.player_clicked[0]
        self.game_state.target_square = self.game_state.player_clicked[1]

        self.game_state.moved_piece = self.board.get_piece(
            self.game_state.moved_square
        )
        self.game_state.target_piece = self.board.get_piece(
            self.game_state.target_square
        )

        self.game_state.move.handle_piece_move(
            self.game_state.moved_square,
            self.game_state.target_square
        )