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
    class Direction(Enum):
        RIGHT = (1, 0)
        DOWN = (0, 1)
        LEFT = (-1, 0)
        UP = (0, -1)

    def __init__(self, width, height):
        self.board = [[random.choice(list(Piece)) for i in range(width)] for j in range(height)]
        self.move_count = 0
        self.curr_piece = self.curr_x, self.curr_y = -1, -1

        self.width = width
        self.height = height

    def get_piece(self, loc):
        x, y = loc
        return self.board[y][x]

    def set_piece(self, loc, value):
        x, y = loc
        self.board[y][x] = value

    def move(self, direction):
        if self.curr_piece < (0, 0):
            return

        new_piece = tuple(i + d for i, d in zip(self.curr_piece, direction))
        if new_piece[0] < 0 or new_piece[0] >= self.width:
            return
        if new_piece[1] < 0 or new_piece[1] >= self.height:
            return

        self._swap(self.curr_piece, new_piece)

    def _swap(self, loc1, loc2):
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
        PADDING = 4
        PIECE_SIZE = 64
        BOARD_SIZE = 6, 5
        GAME_WIDTH = PIECE_SIZE * BOARD_SIZE[0]
        GAME_HEIGHT = PIECE_SIZE * BOARD_SIZE[1]


    def __init__(self):
        super().__init__(PAD.RenderProperties.GAME_WIDTH, PAD.RenderProperties.GAME_HEIGHT)
        self.board = Board(*PAD.RenderProperties.BOARD_SIZE)
        self.mouse_down_prev = False
        self.mouse_loc_prev = (-1, -1)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        mouse_down_curr, _, _ = pygame.mouse.get_pressed()
        mouse_loc_curr = pygame.mouse.get_pos()
        coords_curr = self.pixel_to_coord(*mouse_loc_curr)
        coords_prev = self.pixel_to_coord(*self.mouse_loc_prev)


        if mouse_down_curr and coords_curr != coords_prev:
            direction = tuple(y - x for x, y in zip(coords_prev, coords_curr))
            self.board.move(direction)
            # TODO: Use Direction.
        elif False:
            # TODO: Keyboard
            pass

        # IMPORTANT: Keep this below move.
        if mouse_down_curr:
            self.board.curr_piece = coords_curr
        elif not mouse_down_curr and self.mouse_down_prev:
            self.board.curr_piece = -1, -1

        self.mouse_down_prev = mouse_down_curr
        self.mouse_loc_prev = mouse_loc_curr


    # ---------------------- UTILITY ----------------------

    def pixel_to_coord(self, x, y):
        return (x // PAD.RenderProperties.PIECE_SIZE,
            y // PAD.RenderProperties.PIECE_SIZE)

    def coord_to_pixel(self, i, j):
        return (PAD.RenderProperties.PIECE_SIZE * i + PAD.RenderProperties.PADDING,
            PAD.RenderProperties.PIECE_SIZE * j + PAD.RenderProperties.PADDING)

    def update(self):
        pass

    # ---------------------- RENDERING -----------------------
    def render(self):
        self.screen.fill(Color.BLACK)
        for j in range(PAD.RenderProperties.BOARD_SIZE[1]):
            for i in range(PAD.RenderProperties.BOARD_SIZE[0]):
                if self.board.curr_piece != (i, j):
                    self._draw_piece(i, j)

                if self.board.curr_piece > (-1, -1):
                    self._draw_exact_rect_centered(*pygame.mouse.get_pos())
                
        pygame.display.flip()

    def _draw_piece(self, i, j, trans=False):
        coords = self.coord_to_pixel(i, j)
        self._draw_exact_rect(*coords)

    def _draw_exact_rect(self, x, y):
        coords = self.pixel_to_coord(x, y)
        rect = pygame.Rect(x, y,
                PAD.RenderProperties.PIECE_SIZE - 2 * PAD.RenderProperties.PADDING,
                PAD.RenderProperties.PIECE_SIZE - 2 * PAD.RenderProperties.PADDING)
        pygame.draw.rect(self.screen, self.board.get_piece(coords).get_color(), rect)

    def _draw_exact_rect_centered(self, x, y):
        coords = self.pixel_to_coord(x, y)
        rect = pygame.Rect(
                x - PAD.RenderProperties.PIECE_SIZE / 2,
                y - PAD.RenderProperties.PIECE_SIZE / 2,
                PAD.RenderProperties.PIECE_SIZE - 2 * PAD.RenderProperties.PADDING,
                PAD.RenderProperties.PIECE_SIZE - 2 * PAD.RenderProperties.PADDING)
        pygame.draw.rect(self.screen, self.board.get_piece(coords).get_color(), rect)


if __name__ == '__main__':
    game = PAD()
    game.run()
