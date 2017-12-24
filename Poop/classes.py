from enum import Enum, auto
import random


class ZEnum(Enum):
    # An enum that starts with auto value 0 instead of 1.
    def _generate_next_value_(name, start, count, last_values):
        return count

class Color(ZEnum):
    # Colors of cards.
    RED = auto()
    GREEN = auto()
    BLUE = auto()

class PoopCards(ZEnum):
    # The list of all poop cards
    RED1 = auto()
    RED2 = auto()
    RED3 = auto()
    RED4 = auto()
    GREEN1 = auto()
    GREEN2 = auto()
    GREEN3 = auto()
    GREEN4 = auto()
    BLUE1 = auto()
    BLUE2 = auto()
    BLUE3 = auto()
    BLUE4 = auto()

    def get_color(self):
        # Separate the cards by fours. The cards must be in the same order as colors are
        # defined.
        return Color((self.value) // 4)

class Deck:
    # A deck of cards. Holds both an ordered and unordered list.
    def __init__(self):
        self.cardlist = []
        self.cardcount = [0 for _ in PoopCards]

    def shuffle(self):
        # Fisher-Yates Shuffle
        for i in range(len(self.cardlist))[::-1]:
            idx = random.randint(0, i)
            self.cardlist[idx], self.cardlist[i] = self.cardlist[i], self.cardlist[idx]

    def contains(self, card):
        return 

class Game:
    pass

for card in PoopCards:
    print("{}: {} - {}".format(card.value, card.name, card.get_color()))

