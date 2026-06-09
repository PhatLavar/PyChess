from chess_engine.board import Board
from chess_engine.pieces import Piece
from chess_engine.pieces import Piece
from chess_engine.board import Board
import pygame as pg

class GameState:
    def __init__(self):
        self.white_to_move = True
        self.board = Board()

        self.move_log = []          # ["wP e2->e4", "wP e2->e4 x bP"]
        self.notation = []          # {'moved_piece', 'moved_square', 'target_piece', 'target_square', 'target_prev_piece', 'capture'}

        self.PIECE_IMAGES = {}
        self.selected_square = ()   # (row, col)
        self.player_clicked = []    # [(moved_row, moved_col), (target_row, target_col)]

        self.moved_square = None
        self.moved_piece = None
        self.target_square = None
        self.target_piece = None


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
        
        if (row, col) == self.selected_square or (self.board.board[row][col] == '--' and len(self.player_clicked) == 0):
            self.selected_square = ()
            self.player_clicked = []
        else:
            self.selected_square = (row, col)
            self.player_clicked.append((row, col))
            if len(self.player_clicked) == 2:
                self.moved_square = self.player_clicked[0]
                self.target_square = self.player_clicked[1]
                self.moved_piece = self.board.board[self.moved_square[0]][self.moved_square[1]]
                self.target_piece = self.board.board[self.target_square[0]][self.target_square[1]]
                self.handle_selected_piece_move(self.moved_square, self.target_square)


    def handle_selected_piece_move(self, moved_square, target_square):
        if self.moved_piece == '--':
            self.selected_square = ()
            self.player_clicked = []
            return

        def color_of(piece):
            # 'w' or 'b'
            return None if piece == '--' else piece[0]

        moved_color = color_of(self.moved_piece)
        target_color = color_of(self.target_piece)

        # rule: same color -> no harm, not working for 'castling' yet
        if target_color is not None and moved_color == target_color:
            self.player_clicked = []
            self.selected_square = ()
            self.player_clicked.append(target_square)
            return

        capture = self.target_piece != '--'
        self.board.board[target_square[0]][target_square[1]] = self.moved_piece
        self.board.board[moved_square[0]][moved_square[1]] = '--'

        # record the move and save undo metadata
        self.record_move(self.moved_piece, moved_square, self.target_piece, target_square, capture)
        self.notation.append({
            'moved_piece': self.moved_piece,
            'moved_square': moved_square,
            'target_piece': self.target_piece,
            'target_square': target_square,
            'target_prev_piece': self.target_piece,
            'capture': capture,
        })

        # reset
        self.selected_square = ()
        self.player_clicked = []
        self.white_to_move = not self.white_to_move


    def record_move(self, moved_piece, moved_square, target_piece, target_square, capture, redo = False):
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

        if redo:
            move_log = f"[REDO] {moved_piece} {from_notation}->{to_notation}"
        else:
            move_log = f"{moved_piece} {from_notation}->{to_notation}"

        if capture:
            move_log += f" x {target_piece}"
        
        self.move_log.append(move_log)
        print(move_log)

    
    def handle_undo_move(self):
        if len(self.notation) == 0:
            return

        last_move = self.notation.pop()
        moved_square = last_move['moved_square']
        target_square = last_move['target_square']
        moved_piece = last_move['moved_piece']
        target_prev_piece = last_move['target_prev_piece']

        self.board.board[moved_square[0]][moved_square[1]] = moved_piece
        self.board.board[target_square[0]][target_square[1]] = target_prev_piece

        if len(self.move_log) > 0:
            self.move_log.pop()

        self.record_move(moved_piece, target_square, target_prev_piece, moved_square, last_move['capture'], True)

        self.selected_square = ()
        self.player_clicked = []
        self.white_to_move = not self.white_to_move
