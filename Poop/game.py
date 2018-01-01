from classes import *
import random
import threading
import time
from util import *
import sys

from learner import Network

def random_game_player(game, player):
    while game.gamestate == GameState.ONGOING:
        if game.current_player() == player:
            state = game.get_state(player)
            toilet, pile, lowest, hand = state[0], state[1], state[2], state[3:]

            viable = []
            for i in range(len(hand)):
                if hand[i] > 0:
                    viable.append(i)

            card_idx = random.choice(viable)

            for c in player.deck.cardlist:
                if c.index() == card_idx:
                    card = c
                    break

            res = game.play_card(player, card)

def simple_ai_player(game, player):
    ''' A simple AI to play the game. Plays the highest card it can play without clogging
    the toilet regardless of color. '''

    while game.gamestate == GameState.ONGOING:
        if game.current_player() == player:
            state = game.get_state(player)
            toilet, pile, lowest, hand = state[0], state[1], state[2], state[3:]

            max_playable = toilet - pile - 1
            card_num = Card.POOP_MIN - 1
            card_idx = None
            viable = []
            for i in range(len(hand)):
                if hand[i] > 0:
                    viable.append(i)
                    curr_card_num = i % Card.NUM_CARD_TYPES
                    if curr_card_num > 4:
                        curr_card_num = 0
                    if curr_card_num < max_playable and curr_card_num > card_num:
                        card_idx = i

            if card_idx == None:
                card_idx = random.choice(viable)

            for c in player.deck.cardlist:
                if c.index() == card_idx:
                    card = c
                    break

            game.play_card(player, card)

def expert_ai_player(game, player):
    ''' An AI to play the game. Plays the highest card it can play, tries not to match
    color, and knows when to flush. '''

    while game.gamestate == GameState.ONGOING:
        if game.current_player() == player:
            card = None
            game.play_card(player, card)

def rl_player(game, player):
    with Network("models/move_training/weights.ckpt") as net:
    # with Network("testing/models/tester/weights.ckpt") as net:
        while game.gamestate == GameState.ONGOING:
            if game.current_player() == player:
                state = game.get_state(player)
                toilet, pile, lowest, hand = state[0], state[1], state[2], state[3:]
                card_idx, output = net.get_best_move(state)
                print("State: {}".format(state))
                print("Best: {}".format(card_idx))
                print("Output: {}".format(output))

                chose_random = False
                if hand[card_idx] < 1:
                    chose_random = True
                    viable = []
                    for i in range(len(hand)):
                        if hand[i] > 0:
                            viable.append(i)

                    card_idx = random.choice(viable)

                print("Random: {}".format(chose_random))
                for c in player.deck.cardlist:
                    if c.index() == card_idx:
                        card = c
                        break
                res = game.play_card(player, card)

def play_game(players, targets=None, log_name=None, write=False):
    game = Game(players, log_name)
    threads = []
    if targets == None:
        for player in players:
            t = threading.Thread(target=random_game_player, args=(game, player))
            t.start()
    
    else:
        for player, target in zip(players, targets):
            t = threading.Thread(target=target, args=(game, player))
            t.start()


    winner = None
    try:
        while game.gamestate != GameState.FINISHED:
            pass
        winner = game.current_player()
    except KeyboardInterrupt:
        game.gamestate = GameState.CRASHED
    except Exception:
        game.gamestate = GameState.CRASHED
    finally:
        if write:
            game.logger.write()

        return winner

if __name__ == '__main__':
    # create_games(5000)
    # play_game(players)

    wins = {}
    for p in prompt_players():
        wins[p.name] = 0

    for i in range(100):
        sys.stdout.write("{}/{}\r".format(i, 100))
        players = prompt_players()
        winner = play_game(players, [simple_ai_player, simple_ai_player, simple_ai_player,
            simple_ai_player])

        if winner:
            wins[winner.name] += 1


    for name in wins:
        print("{}: {}".format(name, wins[name]))

