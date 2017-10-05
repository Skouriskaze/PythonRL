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
    # NONE = 5

    def get_color(self):
        if self.value == 0:
            return (255, 0, 0)
        if self.value == 1:
            return (34, 139, 34)
        if self.value == 2:
            return (0, 0, 255)
        if self.value == 3:
            return (255, 255, 0)
        if self.value == 4:
            return (128, 0, 128)
        # if self.value == 5:
            # return (0, 0, 0)

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


    # -------------------- MOVEMENT --------------------
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
        self.move_count += 1

    def _swap(self, loc1, loc2):
        curr = self.get_piece(loc1)
        self.set_piece(loc1, self.get_piece(loc2))
        self.set_piece(loc2, curr)

    # -------------------- BOARD CLEAR --------------------
    def end_turn(self):
        # Consider doing a flood fill/bfs and then grabbing the height and width of each
        # item.
        score = self.clear_combos()
        self.move_count = 0
        return score


    def clear_combos(self):
        visited = []
        hor_match = self._check_horizontal((0, 0), visited)
        
        for orb in hor_match:
            self.set_piece(orb, None)

        self._drop_board()



    def _drop_board(self):
        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                d = 0
                while self.get_piece((i, j + d + 1)) == None:
                    d += 1

                if d:
                    self.set_piece((i, j + d + 1), self.get_piece((i, j)))
                    self.set_piece((i, j), None)


    def _fill_board(self):
        pass

    def _check_horizontal(self, coord, visited):
        # Return a list of horizontal orbs
        x, y = coord
        count = 0
        idp = 1
        idn = 1
        color = self.get_piece(coord)
        ret = []


        while self.get_piece((x + idp, y)) == color:
            count += 1
            idp += 1
        while self.get_piece((x - idn, y)) == color:
            count += 1
            idn += 1

        if count > 2:
            for i in range(idn, idp + 1):
                if (x + i, y) not in visited:
                    ret.append((x + i, y))
                    visited.append((x + i, y))

        return ret

    def _check_vertical(self, coord):
        # Return a list of horizontal orbs
        pass


    # -------------------- DEBUGGING  --------------------
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
        self.old_keys = pygame.key.get_pressed()
        self.mode = 'Mouse'

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        mouse_down_curr, _, _ = pygame.mouse.get_pressed()
        mouse_loc_curr = pygame.mouse.get_pos()
        coords_curr = self.pixel_to_coord(*mouse_loc_curr)
        coords_prev = self.pixel_to_coord(*self.mouse_loc_prev)
        keys = pygame.key.get_pressed()


        if mouse_down_curr and coords_curr != coords_prev:
            self.mode = 'Mouse'
            direction = tuple(y - x for x, y in zip(coords_prev, coords_curr))
            self.board.move(direction)
        elif any(keys):
            self.mode = 'Keyboard'
            if keys[pygame.K_SPACE] and not self.old_keys[pygame.K_SPACE]:
                if self.board.curr_piece < (0, 0):
                    self.board.curr_piece = self.pixel_to_coord(*pygame.mouse.get_pos())
                else:
                    self.board.curr_piece = (-1, -1)

            action = None
            if keys[pygame.K_RIGHT] and not self.old_keys[pygame.K_RIGHT]:
                action = Board.Direction.RIGHT
            elif keys[pygame.K_DOWN] and not self.old_keys[pygame.K_DOWN]:
                action = Board.Direction.DOWN
            elif keys[pygame.K_LEFT] and not self.old_keys[pygame.K_LEFT]:
                action = Board.Direction.LEFT
            elif keys[pygame.K_UP] and not self.old_keys[pygame.K_UP]:
                action = Board.Direction.UP

            if action:
                self.board.move(action.value)
                new_piece = tuple(i + d for i, d in zip(self.board.curr_piece, action.value))
                if new_piece[0] < 0 or new_piece[0] >= self.board.width:
                    return
                if new_piece[1] < 0 or new_piece[1] >= self.board.height:
                    return
                self.board.curr_piece = new_piece

        # IMPORTANT: Keep this below move.
        if mouse_down_curr:
            self.board.curr_piece = coords_curr
        elif not mouse_down_curr and self.mouse_down_prev:
            self.board.curr_piece = -1, -1
            # self.board.end_turn()

        self.mouse_down_prev = mouse_down_curr
        self.mouse_loc_prev = mouse_loc_curr
        self.old_keys = keys


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

                if self.mode == 'Mouse':
                    if self.board.curr_piece > (-1, -1):
                        self._draw_exact_piece(*pygame.mouse.get_pos())
                else:
                    if self.board.curr_piece > (-1, -1):
                        self._draw_piece(*self.board.curr_piece)

                
        pygame.display.flip()

    def _draw_piece(self, i, j, trans=False):
        coords = self.coord_to_pixel(i, j)
        self._draw_exact_piece(*tuple(x + PAD.RenderProperties.PIECE_SIZE // 2 for x in coords))

    def _draw_exact_piece(self, x, y):
        coords = self.pixel_to_coord(x, y)
        pygame.draw.circle(self.screen, self.board.get_piece(coords).get_color(),
                (x, y),
                (PAD.RenderProperties.PIECE_SIZE - 2 * PAD.RenderProperties.PADDING) // 2)


if __name__ == '__main__':
    game = PAD()
    game.run()
