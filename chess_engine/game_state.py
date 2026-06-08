from chess_engine.board import Board
from chess_engine.pieces import Piece
from chess_engine.pieces import Piece
from chess_engine.board import Board
import pygame as pg

class GameState:
    def __init__(self):
        self.white_to_move = True
        self.board = Board()
        self.move_log = []

        self.PIECE_IMAGES = {}
        self.selected_square = ()
        self.player_clicked = []


    def load_piece_images(self):
        for piece in Piece.PIECES:
            self.PIECE_IMAGES[piece] = pg.transform.scale(
                pg.image.load(f'assets/images/chess_pieces/{piece}.png'), 
                (self.board.SQUARE_SIZE, self.board.SQUARE_SIZE)
            )


    def draw_game_state(self, screen):
        def draw_board(screen):
            colors = [pg.Color('white'), pg.Color('gray')]
            for row in range(self.board.DIMENSION):
                for col in range(self.board.DIMENSION):
                    pg.draw.rect(
                        screen, 
                        colors[(row + col) % 2], 
                        pg.Rect(
                            col * self.board.SQUARE_SIZE, 
                            row * self.board.SQUARE_SIZE, 
                            self.board.SQUARE_SIZE, 
                            self.board.SQUARE_SIZE
                        )
                    )

        def draw_pieces(screen, board):
            for row in range(self.board.DIMENSION):
                for col in range(self.board.DIMENSION):
                    piece = board[row][col]
                    if piece != '--':
                        screen.blit(
                            self.PIECE_IMAGES[piece], 
                            pg.Rect(
                                col * self.board.SQUARE_SIZE, 
                                row * self.board.SQUARE_SIZE, 
                                self.board.SQUARE_SIZE, 
                                self.board.SQUARE_SIZE 
                            )
                        )

        draw_board(screen)
        draw_pieces(screen, self.board.board)


    def handle_mouse_click(self, mouse_location):
        col = mouse_location[0] // self.board.SQUARE_SIZE
        row = mouse_location[1] // self.board.SQUARE_SIZE
        
        if (row, col) == self.selected_square:
            self.selected_square = ()
            self.player_clicked = []
        else:
            self.selected_square = (row, col)
            self.player_clicked.append((row, col))
            if len(self.player_clicked) == 2:
                self.handle_selected_piece_move(self.player_clicked[0], self.player_clicked[1])


    def handle_selected_piece_move(self, moved_square, target_square):
        moved_piece = self.board.board[moved_square[0]][moved_square[1]]
        target_piece = self.board.board[target_square[0]][target_square[1]]

        if moved_piece == '--':
            self.selected_square = ()
            self.player_clicked = []
            return

        def color_of(piece):
            # 'w' or 'b'
            return None if piece == '--' else piece[0]

        moved_color = color_of(moved_piece)
        target_color = color_of(target_piece)

        # rule: same color -> no harm
        if target_color is not None and moved_color == target_color:
            print(f"Illegal move: same color at target ({moved_piece} -> {target_piece})")
            self.selected_square = ()
            self.player_clicked = []
            return

        capture = target_piece != '--'
        self.board.board[target_square[0]][target_square[1]] = moved_piece
        self.board.board[moved_square[0]][moved_square[1]] = '--'

        # record the move and print notation
        self.record_move(moved_piece, moved_square, target_piece, target_square, capture)

        # reset
        self.selected_square = ()
        self.player_clicked = []
        self.white_to_move = not self.white_to_move

    def record_move(self, moved_piece, moved_square, target_piece, target_square, capture):
        """
        Format, store and print a simple move notation.
        Example: 'wP e2->e4' or 'wP e2->e4 x bP' when capturing.
        """
        def square_to_notation(square):
            files = 'abcdefgh'
            row, col = square
            file = files[col]
            rank = str(self.board.DIMENSION - row)
            return f"{file}{rank}"

        from_notation = square_to_notation(moved_square)
        to_notation = square_to_notation(target_square)

        notation = f"{moved_piece} {from_notation}->{to_notation}"
        if capture:
            notation += f" x {target_piece}"

        self.move_log.append(notation)
        print(notation)
