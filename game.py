# Write your code here

import numpy as np


class TetrisGrid:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.matrix = np.full([height, width], "-", dtype=str)
        self.piece = None
        self.x = 0
        self.y = 0

    def __str__(self):
        string = ''
        for row in self.matrix:
            string += ' '.join(map(str, row)) + '\n'
        return string

    def update_grid(self):
        self.matrix = np.full([self.height, self.width], "-", dtype=str)
        if self.piece:
            # fill piece's pixels in the matrix
            for pixel in self.piece.matrices[self.piece.position]:
                self.matrix[int(pixel / self.width)][pixel % self.width] = '0'

        self.matrix = np.roll(self.matrix, self.y, axis=0)
        self.matrix = np.roll(self.matrix, self.x, axis=1)

        # check if bottom is reached
        if any(self.matrix[self.height - 1][i] == '0' for i in range(self.width)):
            self.piece.static = True

    def ensure_lively(func):
        def inner(self):
            if not self.piece.static:
                func(self)
        return inner

    @ensure_lively
    def move_left(self):
        # ensure no pixels on border
        if all(self.matrix[i][0] == '-' for i in range(self.height)):
            self.x -= 1
        self.move_down()

    @ensure_lively
    def move_right(self):
        # ensure no pixels on border
        if all(self.matrix[i][self.width - 1] == '-' for i in range(self.height)):
            self.x += 1
        self.move_down()

    @ensure_lively
    def move_down(self):
        self.y += 1
        self.update_grid()

    @ensure_lively
    def rotate_piece(self):
        self.piece.left_roll()
        self.update_grid()
        self.move_down()

    def load_piece(self, piece):
        self.piece = piece
        self.update_grid()


class TetrisPiece:
    def __init__(self):
        self.matrices = []
        self.position = 0
        self.static = False

    def left_roll(self):
        self.position = (self.position + 1) % len(self.matrices)
        # self.matrix = np.rot90(self.matrix)
        # self.matrix = np.roll(self.matrix, -1, axis=0)
        # self.matrix = np.roll(self.matrix, -1, axis=1)


class IPiece(TetrisPiece):
    def __init__(self):
        super(IPiece, self).__init__()
        self.matrices = [[4, 14, 24, 34], [3, 4, 5, 6]]
        self.matrix = np.array([['-', '0', '-', '-'], ['-', '0', '-', '-'], ['-', '0', '-', '-'], ['-', '0', '-', '-']])

    # def left_roll(self):
    #     self.matrix = np.rot90(self.matrix)


class SPiece(TetrisPiece):
    def __init__(self):
        super(SPiece, self).__init__()
        self.matrices = [[5, 4, 14, 13], [4, 14, 15, 25]]
        self.matrix = np.array([['-', '-', '-', '-'], ['-', '0', '0', '-'], ['0', '0', '-', '-'], ['-', '-', '-', '-']])


class ZPiece(TetrisPiece):
    def __init__(self):
        super(ZPiece, self).__init__()
        self.matrices = [[4, 5, 15, 16], [5, 15, 14, 24]]
        self.matrix = np.array([['-', '-', '-', '-'], ['0', '0', '-', '-'], ['-', '0', '0', '-'], ['-', '-', '-', '-']])


class LPiece(TetrisPiece):
    def __init__(self):
        super(LPiece, self).__init__()
        self.matrices = [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]
        self.matrix = np.array([['-', '0', '-', '-'], ['-', '0', '-', '-'], ['-', '0', '0', '-'], ['-', '-', '-', '-']])


class JPiece(TetrisPiece):
    def __init__(self):
        super(JPiece, self).__init__()
        self.matrices = [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]


class OPiece(TetrisPiece):
    def __init__(self):
        super(OPiece, self).__init__()
        self.matrices = [[4, 14, 15, 5]]
        self.matrix = np.array([['-', '-', '-', '-'], ['-', '0', '0', '-'], ['-', '0', '0', '-'], ['-', '-', '-', '-']])


class TPiece(TetrisPiece):
    def __init__(self):
        super(TPiece, self).__init__()
        self.matrices = [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]
        self.matrix = np.array([['-', '0', '-', '-'], ['0', '0', '0', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']])


def select_piece(symbol):
    switch = {
        'I': IPiece,
        'S': SPiece,
        'Z': ZPiece,
        'L': LPiece,
        'J': JPiece,
        'O': OPiece,
        'T': TPiece,
    }
    return switch.get(symbol)


def run():
    piece = select_piece(input())()
    grid = TetrisGrid(*map(lambda x: int(x), input().split()))
    print(grid)
    grid.load_piece(piece)
    print(grid)

    while True:
        # command = input("Input command: ")
        command = input()

        if command == "left":
            grid.move_left()
            print(grid)

        elif command == "right":
            grid.move_right()
            print(grid)

        elif command == "rotate":
            grid.rotate_piece()
            print(grid)

        elif command == "down":
            grid.move_down()
            print(grid)

        elif command == "exit":
            break


# do run
run()
