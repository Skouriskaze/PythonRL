from game import Game
from enum import Enum
import random

class Piece(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2
    YELLOW = 3
    DARK = 4

class Board:
    width = 6
    height = 5
    def __init__(self):
        self.board = [[random.choice(list(Piece)) for _ in range(Board.width)] for _ in range(Board.height)]
        self.move_count = 0
        self.curr_piece = self.curr_x, self.curr_y = 0, 0

    def get_piece(self, loc):
        x, y = loc
        return self.board[y][x]

    def set_piece(self, loc, value):
        x, y = loc
        self.board[y][x] = value

    def swap(self, loc1, loc2):
        curr = self.get_piece(loc1)
        self.set_piece(loc1, self.get_piece(loc2))
        self.set_piece(loc2, curr)

    def end_board(self):
        # return score
        return 0


    def __repr__(self):
        s = ""
        for x in self.board:
            s += (' '.join([str(a) for a in x]))
            s += '\n'

        return s

    def __str__(self):
        s = ""
        for x in self.board:
            s += (' '.join([str(a.value) for a in x]))
            s += '\n'

        return s


class PAD(Game):

    def update(self):
        pass

if __name__ == '__main__':
    b = Board()
    b.swap((0, 0), (0, 1))
    print(b)
