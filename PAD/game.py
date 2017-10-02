import pygame
from enum import Enum
import sys

class Color:
    BLACK = (0, 0, 0)


class Game:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

    def run(self):
        while 1:
            self.process_events()
            self.update()
            self.render()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


    def render(self):
        self.screen.fill(Color.BLACK)
        pygame.display.flip()

    def update(self):
        pass

if __name__ == '__main__':
    g = Game(320, 240)
    g.run()
