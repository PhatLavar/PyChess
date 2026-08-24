from chess_engine.moves.execution.move_executor import MoveExecutor
from chess_engine.utilities import EMP, piece_color, turn_color
from chess_ui.config import SQUARE_SIZE
from chess_ui.screens import PromotionUI


class InputHandler:
    """Translate mouse input into engine moves and UI selection state."""

    NO_SQUARE = ()
    MOVE_SELECTION_SIZE = 2
    LATEST_MOVE_INDEX = -1

    def __init__(self, game_state, move_animation):
        """Create empty selection state for the supplied match."""
        self.game_state = game_state
        self.move_animation = move_animation
        self.promotion_ui = PromotionUI(game_state)

        self.selected_square = self.NO_SQUARE
        self.player_clicked = []
        self.hovered_square = None
        self.selected_legal_moves = []

    @property
    def board(self):
        """Return the active engine board."""
        return self.game_state.board

    # Mouse input

    def handle_mouse_click(self, mouse_location):
        """Process a board or promotion click.

        Returns:
            ``True`` when a move or promotion changed engine state; otherwise
            ``False``.
        """
        if self.game_state.game_over or self.move_animation.is_animating:
            return False

        if self.game_state.promotion_pending:
            return self._handle_promotion_click(mouse_location)

        square = self._get_square(mouse_location)
        piece = self.board.get_piece(square)

        if self._should_reset_selection(square, piece):
            self.reset_selection()
            return False

        self._select_square(square)

        if len(self.player_clicked) == self.MOVE_SELECTION_SIZE:
            return self._execute_selected_move()

        return False

    def handle_mouse_motion(self, mouse_location):
        """Update board hover state, or clear it while a modal is active."""
        if self.game_state.game_over or self.game_state.promotion_pending:
            self.hovered_square = None
            return

        self.hovered_square = self._get_square(mouse_location)

    def handle_undo(self):
        """Stop animation, request undo, and return whether state changed."""
        self.move_animation.stop()
        state_changed = self.game_state.move.handle_undo_move()

        if state_changed:
            self.reset_selection()

        return state_changed

    # Selection

    def reset_selection(self):
        """Clear selected squares and legal-move highlights."""
        self.selected_square = self.NO_SQUARE
        self.player_clicked = []
        self.selected_legal_moves = []

    def _get_square(self, mouse_location):
        """Convert a pixel position to a ``(row, column)`` board square."""
        col = mouse_location[0] // SQUARE_SIZE
        row = mouse_location[1] // SQUARE_SIZE
        return row, col

    def _should_reset_selection(self, square, piece):
        """Return whether the click should cancel the current selection."""
        if square == self.selected_square:
            return True

        if self.player_clicked:
            return False

        return (
            piece == EMP
            or piece_color(piece) != turn_color(self.game_state.white_to_move)
        )

    def _select_square(self, square):
        """Select a square and refresh its legal target highlights."""
        self.selected_square = square
        self.player_clicked.append(square)
        self.selected_legal_moves = [
            target_square
            for moved_square, target_square in self.game_state.move.get_valid_moves()
            if moved_square == square
        ]

    # Move execution

    def _execute_selected_move(self):
        """Submit the selected move and translate its outcome into UI state."""
        moved_square, target_square = self.player_clicked
        outcome = self.game_state.move.handle_piece_move(
            moved_square,
            target_square,
        )

        if outcome == MoveExecutor.SAME_COLOR:
            self.reset_selection()
            self._select_square(target_square)
            return False

        if outcome == MoveExecutor.MOVED:
            self._animate_latest_move()
            self.reset_selection()
            return True

        if outcome == MoveExecutor.PROMOTION_PENDING:
            self.reset_selection()
            return False

        self.reset_selection()
        return False

    def _handle_promotion_click(self, mouse_location):
        """Apply a clicked promotion choice and start its animation."""
        chosen_type = self.promotion_ui.get_choice(mouse_location)

        if chosen_type is None:
            return False

        state_changed = self.game_state.move.executor.handle_pawn_promotion(
            chosen_type
        )

        if state_changed:
            self._animate_latest_move()
            self.reset_selection()

        return state_changed

    def _animate_latest_move(self):
        """Create UI animations from the latest engine history record."""
        if not self.game_state.move.notation:
            return

        move = self.game_state.move.notation[self.LATEST_MOVE_INDEX]
        animated_piece = move.get('promotion_piece', move['moved_piece'])

        self.move_animation.start(
            animated_piece,
            move['moved_square'],
            move['target_square'],
        )

        if move.get('castling'):
            self.move_animation.start(
                move['rook_piece'],
                move['rook_square'],
                move['rook_target_square'],
            )
