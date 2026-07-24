import pygame as pg


class MoveAnimation:
    def __init__(self, game_state):
        self.game_state = game_state

        self.is_animating = False
        self.piece = None
        self.start_square = None
        self.end_square = None

        self.start_time = 0
        self.duration = 200  # milliseconds
        self.animations = []

    @property
    def board(self):
        return self.game_state.board

    def start(self, piece, start_square, end_square):
        self.animations.append({
            'piece': piece,
            'start_square': start_square,
            'end_square': end_square,
            'start_time': pg.time.get_ticks(),
        })
        self.is_animating = True
        self.piece = piece
        self.start_square = start_square
        self.end_square = end_square
        self.start_time = pg.time.get_ticks()

    def stop(self):
        self.is_animating = False
        self.animations = []
        self.piece = None
        self.start_square = None
        self.end_square = None
        self.start_time = 0

    def draw(self, screen):
        if not self.animations:
            self.is_animating = False
            return

        current_time = pg.time.get_ticks()
        active_animations = []

        for animation in self.animations:
            progress = min((current_time - animation['start_time']) / self.duration, 1)

            if progress >= 1:
                continue

            x, y = self._interpolate_position(animation, progress)
            piece_image = self.game_state.PIECE_IMAGES.get(animation['piece'])

            if piece_image is not None:
                screen.blit(piece_image, (x, y))

            active_animations.append(animation)

        self.animations = active_animations
        self.is_animating = bool(self.animations)

        if self.is_animating:
            first_animation = self.animations[0]
            self.piece = first_animation['piece']
            self.start_square = first_animation['start_square']
            self.end_square = first_animation['end_square']
            self.start_time = first_animation['start_time']
        else:
            self.piece = None
            self.start_square = None
            self.end_square = None
            self.start_time = 0

    def should_skip_piece(self, square):
        if not self.animations:
            return False

        return any(animation['end_square'] == square for animation in self.animations)

    def _interpolate_position(self, animation, progress):
        start_row, start_col = animation['start_square']
        end_row, end_col = animation['end_square']

        square_size = self.board.SQUARE_SIZE

        start_x = start_col * square_size
        start_y = start_row * square_size
        end_x = end_col * square_size
        end_y = end_row * square_size

        current_x = start_x + (end_x - start_x) * progress
        current_y = start_y + (end_y - start_y) * progress

        return current_x, current_y