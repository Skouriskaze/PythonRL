from Logger import *
from enum import Enum, auto

import datetime
import random
import re
import util


class Color(Enum):
    '''
    Colors of cards.
    '''

    RED = auto()
    GREEN = auto()
    BLUE = auto()


class CardType(Enum):
    '''
    Playing Card types
    '''
    POOP = auto()
    SKIP = auto()


class PlayerType(Enum):
    '''
    Player Input Types
    '''
    HUMAN = auto()
    COMPUTER = auto()


class GameState(Enum):
    ''' Game States'''
    ONGOING = auto()
    FINISHED = auto()
    CRASHED = auto()

class Card:
    '''
    A card. Has a color, number, and type
    '''
    POOP_MIN = 0 # Minimum number on poop card, inclusive
    POOP_MAX = 5 # Maximum number on poop card, exclusive
    NUM_CARD_TYPES = 6
    TOTAL_CARDS = 18 # Total different number of cards
    def __init__(self, color, number, ctype):
        ''' Sets the color, number, and type of a card '''
        self.color = color
        self.number = number
        self.ctype = ctype

    def _rel_index(self):
        ''' Gets the relative index of a card (color-agnostic) '''
        if self.ctype == CardType.POOP:
            return self.number - Card.POOP_MIN
        else:
            return Card.POOP_MAX - Card.POOP_MIN + self.ctype.value - 2

    def index(self):
        ''' Gets the index of a card '''
        return (self.color.value - 1) * Card.NUM_CARD_TYPES + self._rel_index()

    def __str__(self):
        value = self.ctype if self.ctype != CardType.POOP else self.number
        return "{} {}".format(self.color.name, value)


class Toilet:
    '''
    A toilet card
    '''
    TOILET_MIN = 8 # Minimum number on toilet card, inclusive
    TOILET_MAX = 15 # Maximum number on toilet card, exclusive
    def __init__(self, color, number):
        ''' Sets the number and color of a toilet '''
        self.number = number
        self.color = color

    def __str__(self):
        return "Toilet: {} {}".format(self.color.name, self.number)


class SimpleDeck:
    ''' A deck of toilet cards '''

    def __init__(self):
        self.cardlist = []
    
    def shuffle(self):
        ''' Shuffles the deck '''
        util.shuffle(self.cardlist)

    def contains(self, card):
        ''' Checks whether a card is in the deck '''
        return card in self.cardlist

    def draw(self):
        ''' Returns the top card of a deck '''
        try:
            card = self.cardlist.pop(0)
            return card
        except IndexError:
            return None

    def remove(self, card):
        ''' Removes a card from a deck '''
        if self.cardcount[card.index()] > 0:
            self.cardlist.remove(card)

    def insert_card(self, card, location=0):
        ''' Inserts a card into a deck. Defaults to the top. '''
        self.cardlist.insert(location, card)

    def add_cards(self, cards):
        ''' Add a list of cards to a deck Defaults to the bottom '''
        self.cardlist = self.cardlist + cards

    def clear(self):
        ''' Clears the deck '''
        self.cardlist = []

class Deck(SimpleDeck):
    '''
    A deck of cards. Holds both an ordered and unordered list. Used for decks, discard
    piles, hands... 0 is the top, n is the bottom.
    '''

    def __init__(self):
        '''
        Deck setup
        '''
        self.clear()

    def remove(self, card):
        ''' Removes a card from a deck '''
        if self.cardcount[card.index()] > 0:
            self.cardcount[card.index()] -= 1
            self.cardlist.remove(card)

    def insert_card(self, card, location=0):
        ''' Inserts a card into a deck. Defaults to the top. '''
        self.cardlist.insert(location, card)
        self.cardcount[card.index()] += 1

    def add_cards(self, cards):
        ''' Add a list of cards to a deck Defaults to the bottom '''
        for card in cards:
            self.cardcount[card.index()] += 1
        self.cardlist = self.cardlist + cards

    def clear(self):
        ''' Clears the deck '''
        self.cardlist = []
        self.cardcount = [0 for _ in range(Card.TOTAL_CARDS)]


    def __iter__(self):
        return iter(self.cardlist)
    def __repr__(self):
        return self.cardcount
    def __str__(self):
        # return str([PoopCards(card).name for card in self.cardlist])
        s = str(self.cardcount[:Card.NUM_CARD_TYPES]) + '\n'
        s += str(self.cardcount[Card.NUM_CARD_TYPES:2*Card.NUM_CARD_TYPES]) + '\n'
        s += str(self.cardcount[Card.NUM_CARD_TYPES*2:])
        return s
        

class Player:
    ''' A player '''
    def __init__(self, name, pid, ptype):
        ''' Player information '''
        self.deck = Deck()
        self.name = name
        self.pid = pid
        self.ptype = ptype


    def broadcast(self, msg):
        ''' Broadcasts a message to the player '''
        if self.ptype == PlayerType.HUMAN:
            print(msg)

    def __str__(self):
        return self.name


class Game:
    ''' The game logic and information '''

    # These are types of turns that can happen
    INVALID = -1
    STANDARD = 0
    FLUSH = 1
    WIN = 2

    TOILET_REPEATS = 1 # Number of toilet cards per capacity

    POOP_REPEATS = 4 # Number of poop cards per number
    SPECIAL_REPEATS = 2

    NUM_CARDS_START = 5 # Number of cards to start in a hand

    NUM_CARDS_FLUSH = 3

    def __init__(self, players):
        '''
        Game setup
        '''
        # Game Setup
        self.gamestate = GameState.ONGOING
        today = datetime.datetime.today()
        self.logger = Logger("{:04}{:02}{:02} {:02}{:02}{:02}".format(today.year, today.month,
            today.day, today.hour, today.minute, today.second))

        # Player Setup
        self.num_players = len(players)
        self.players = players
        self.turn = 0

        # Pile Card Setup
        self.pile = Deck()
        self.pile_count = 0

        self.trash = Deck()

        # Toilet Setup
        self.toilet_cards = self.initialize_toilet_deck()
        self.draw_toilet()

        # Deck Setup
        self.deck = self.initialize_poop_deck()
        for _ in range(Game.NUM_CARDS_START):
            for player in self.players:
                self.draw(player, self.deck)
        self.logger.add_blank()

    def current_player(self):
        ''' Returns the player whose turn it is '''
        return self.players[self.turn]

    def initialize_poop_deck(self):
        ''' Populate the initial poop deck '''
        deck = Deck()
        for color in Color:
            for _ in range(Game.POOP_REPEATS):
                deck.add_cards([Card(color, num, CardType.POOP) for num in range(Card.POOP_MIN,
                    Card.POOP_MAX)])
            for _ in range(Game.SPECIAL_REPEATS):
                deck.insert_card(Card(color, 0, CardType.SKIP))

        deck.shuffle()
        return deck

    def initialize_toilet_deck(self):
        ''' Populate the initial toilet deck '''
        deck = SimpleDeck()
        for _ in range(Game.TOILET_REPEATS):
            for color in Color:
                deck.add_cards([Toilet(color, num) for num in range(Toilet.TOILET_MIN,
                    Toilet.TOILET_MAX)])

        deck.shuffle()
        return deck

    def draw_toilet(self):
        ''' Draws a new toilet '''
        self.toilet = self.toilet_cards.draw()
        self.logger.add_toilet(self.toilet)
        self.broadcast_all("A new toilet has been drawn: {}".format(self.toilet))


    def draw(self, player, deck):
        '''
        Given player draws a card from given deck
        '''
        card = deck.draw()
        if card == None:
            raise IndexError("There are no cards left!")
        player.deck.insert_card(card)
        self.logger.add_draw(player, card)
        self.broadcast(player, "{}, you have drawn {}".format(player.name, card))
        return card

    def pass_turn(self):
        '''
        Ends the current turn
        '''
        self.turn += 1
        self.turn %= self.num_players

    def flush(self, player):
        ''' Executes toilet flush logic '''
        self.trash.add_cards(self.pile.cardlist)
        self.pile.clear()
        self.pile_count = 0
        for oplayer in self.players:
            if oplayer != player:
                self.draw(oplayer, self.deck)
        self.logger.add_flush(player)
        self.broadcast_all("{} flushed the toilet.".format(player.name))

        if len(player.deck.cardlist) == 0:
            self.gamestate = GameState.FINISHED
            self.logger.add_win(player)
            return Game.WIN
        return Game.FLUSH

    def clog(self, player):
        ''' Executes toilet clog logic '''
        player.deck.add_cards(self.pile.cardlist)
        self.toilet = self.toilet_cards.draw()
        self.pile.clear()
        self.pile_count = 0

        self.logger.add_clog(player)
        self.broadcast_all("{} clogged the toilet.".format(player.name))
        self.pass_turn()

        return Game.STANDARD

    def play_card(self, player, card):
        '''
        A player's turn to go. If the player is not the current turn or if the player
        tries to play a card he does not have, then the game breaks??
        '''
        # Invalid moves
        if player.pid != self.turn:
            self.broadcast_all("It was not {}'s turn.".format(player.name))
            return Game.INVALID
        if not player.deck.contains(card):
            self.broadcast_all("{} could not play {}".format(player.name, card))
            return Game.INVALID

        # Playing the card into the pile
        player.deck.remove(card)
        self.pile.insert_card(card)
        self.pile_count += card.number

        self.logger.add_move(player, card)
        self.broadcast_all("[{}] {} played {}. The pile is now at {}".format(self.toilet,
            player.name, card, self.pile_count))

        # Game Logic and Return Values
        if len(self.pile.cardlist) >= Game.NUM_CARDS_FLUSH:
            top = [card.color for card in self.pile.cardlist[:Game.NUM_CARDS_FLUSH]]
            if top.count(top[0]) == Game.NUM_CARDS_FLUSH:
                return self.flush(player)

        if self.pile_count >= self.toilet.number:
            return self.clog(player)


        if len(player.deck.cardlist) == 0:
            # Game win
            self.gamestate = GameState.FINISHED
            self.logger.add_win(player)
            return Game.WIN

        self.pass_turn()
        return Game.STANDARD

    def get_state(self, player):
        ''' Gets the current state of the game from a player's perspective '''
        return [self.toilet.number] + [self.pile_count] + player.deck.cardcount

    def broadcast(self, player, msg):
        ''' Broadcasts a message to a player '''
        player.broadcast(msg)

    def broadcast_all(self, msg):
        ''' Broadcasts a message to all players '''
        for player in self.players:
            player.broadcast(msg)

