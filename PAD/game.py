import pygame
from enum import Enum
import sys

class Color(Enum):
    BLACK = (0, 0, 0)


class Game:
    size = x, y = 320, 240
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Game.size)

    def run(self):
        while 1:
            self.update()
            self.render()

    def render(self):
        self.screen.fill(Color.BLACK)
        self.screen.flip()

    def update(self):
        pass

if __name__ == '__main__':
    g = Game()
    g.run()
