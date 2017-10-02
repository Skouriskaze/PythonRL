from game import Game, Color
from enum import Enum
import pygame
import random
import sys

class Piece(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2
    YELLOW = 3
    DARK = 4

    def get_color(self):
        if self.value == 0:
            return (255, 0, 0)
        if self.value == 1:
            return (0, 255, 0)
        if self.value == 2:
            return (0, 0, 255)
        if self.value == 3:
            return (0, 255, 255)
        if self.value == 4:
            return (255, 0, 255)

class Board:
    def __init__(self, width, height):
        self.board = [[random.choice(list(Piece)) for _ in range(width)] for _ in range(height)]
        self.move_count = 0
        self.curr_piece = self.curr_x, self.curr_y = 0, 0

        self.width = width
        self.height = height

    def get_piece(self, loc):
        x, y = loc
        return self.board[y][x]

    def set_piece(self, loc, value):
        x, y = loc
        self.board[y][x] = value

    def move(self, loc1, loc2):
        curr = self.get_piece(loc1)
        self.set_piece(loc1, self.get_piece(loc2))
        self.set_piece(loc2, curr)

    def end_turn(self):
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
    class RenderProperties:
        PADDING = 2
        PIECE_SIZE = 64
        BOARD_SIZE = 6, 5
        GAME_WIDTH = PIECE_SIZE * BOARD_SIZE[0]
        GAME_HEIGHT = PIECE_SIZE * BOARD_SIZE[1]


    def __init__(self):
        super().__init__(PAD.RenderProperties.GAME_WIDTH, PAD.RenderProperties.GAME_HEIGHT)
        self.board = Board(*PAD.RenderProperties.BOARD_SIZE)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        m1, _, _ = pygame.mouse.get_pressed()
        if m1:
            i, j = self.pixel_to_coord(*pygame.mouse.get_pos())
            # TODO

    def pixel_to_coord(self, x, y):
        return (x // PAD.RenderProperties.PIECE_SIZE,
            y // PAD.RenderProperties.PIECE_SIZE)

    def coord_to_pixel(self, i, j):
        return (PAD.RenderProperties.PIECE_SIZE * i + PAD.RenderProperties.PADDING,
            PAD.RenderProperties.PIECE_SIZE * j + PAD.RenderProperties.PADDING)

    def update(self):
        pass

    def render(self):
        self.screen.fill(Color.BLACK)
        for j in range(PAD.RenderProperties.BOARD_SIZE[1]):
            for i in range(PAD.RenderProperties.BOARD_SIZE[0]):
                self._draw_piece(i, j)
                
        pygame.display.flip()

    def _draw_piece(self, i, j, trans=False):
        coords = self.coord_to_pixel(i, j)
        rect = pygame.Rect(coords[0], coords[1],
                PAD.RenderProperties.PIECE_SIZE - 2 * PAD.RenderProperties.PADDING,
                PAD.RenderProperties.PIECE_SIZE - 2 * PAD.RenderProperties.PADDING)
        pygame.draw.rect(self.screen, self.board.get_piece((i, j)).get_color(), rect)


if __name__ == '__main__':
    game = PAD()
    game.run()
