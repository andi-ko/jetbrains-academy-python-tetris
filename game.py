# Write your code here

import numpy as np

class TetrisGrid:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.matrix = np.full([height, width], "-", dtype=str)
        self.piece = None

    def __str__(self):
        string = ''
        for row in self.matrix:
            string += ' '.join(map(str, row)) + '\n'
        return string

    def check_static(func):
        def inner(self):
            if not self.piece.static:
                # check if bottom is reached
                if any(int(pixel / self.width) == self.height - 1 for
                       pixel in self.piece.matrices[self.piece.position]):
                    self.piece.static = True
                # check if other piece is touched
                else:
                    # remove current piece from board to make check easier
                    self.wipe_piece()
                    if any(self.matrix[int(pixel / self.width) + 1][pixel % self.width] == '0' for
                            pixel in self.piece.matrices[self.piece.position]):
                        self.piece.static = True
                    self.set_piece()
                if not self.piece.static:
                    func(self)
        return inner

    def check_alive(func):
        def inner(self, *args):
            global alive
            func(self, *args)
            if any(all(self.matrix[j][i] == '0' for j in range(self.height))
                    for i in range(self.width)):
                alive = False
        return inner

    def set_piece(self):
        if self.piece:
            # fill piece's pixels in the matrix
            for pixel in self.piece.matrices[self.piece.position]:
                self.matrix[int(pixel / self.width)][pixel % self.width] = '0'

    def wipe_piece(self):
        if self.piece:
            # remove piece's pixels in the matrix
            for pixel in self.piece.matrices[self.piece.position]:
                self.matrix[int(pixel / self.width)][pixel % self.width] = '-'

    @check_alive
    @check_static
    def move_left(self):
        self.wipe_piece()
        # ensure no pixels on left border
        if all(pixel % self.width != 0 for
                pixel in self.piece.matrices[self.piece.position]):
            # shift pixels
            self.piece.matrices = list(map(
                lambda x: list(map(lambda y: y - 1, x)), self.piece.matrices))
        self.set_piece()
        self.move_down()

    @check_alive
    @check_static
    def move_right(self):
        self.wipe_piece()
        # ensure no pixels on right border
        if all(pixel % self.width != self.width - 1 for
                pixel in self.piece.matrices[self.piece.position]):
            # shift pixels
            self.piece.matrices = list(map(
                lambda x: list(map(lambda y: y + 1, x)), self.piece.matrices))
        self.set_piece()
        self.move_down()

    @check_alive
    @check_static
    def move_down(self):
        self.wipe_piece()
        # shift pixels
        self.piece.matrices = list(map(
            lambda x: list(map(lambda y: y + self.width, x)), self.piece.matrices))
        self.set_piece()

    @check_alive
    @check_static
    def rotate_piece(self):
        self.wipe_piece()
        self.piece.left_roll()
        self.set_piece()
        self.move_down()

    def roll_grid(self):
        # clear last row
        for i in range(self.width):
            self.matrix[self.height - 1][i] = "-"
        self.matrix = np.roll(self.matrix, 1, axis=0)

    def clear_rows(self):
        while all(self.matrix[self.height - 1][i] == '0' for i in range(self.width)):
            if self.piece:
                if any(int(pixel / self.width) == self.height - 1 for
                        pixel in self.piece.matrices[self.piece.position]):
                    self.piece = None
                else:
                    self.move_down()
                    self.wipe_piece()
            self.roll_grid()
            if self.piece:
                self.set_piece()

    def load_piece(self, piece):
        if not self.piece or self.piece.static:
            self.piece = piece
            self.set_piece()


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


alive = True


def run():
    grid = TetrisGrid(*map(lambda x: int(x), input().split()))
    print(grid)

    while alive:
        # command = input("Input command: ")
        command = input()

        if command == "piece":
            grid.load_piece(select_piece(input())())
            print(grid)

        elif command == "left":
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

        elif command == "break":
            grid.clear_rows()
            print(grid)

        elif command == "exit":
            break

    print("Game Over!")


# do run
run()
