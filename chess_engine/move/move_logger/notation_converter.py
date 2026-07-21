class NotationConverter:
    def __init__(self, board):
        self.board = board

    def square_to_notation(self, square):
        files = 'abcdefgh'
        row, col = square
        file = files[col]
        rank = str(self.board.DIMENSION - row)
        return f"{file}{rank}"