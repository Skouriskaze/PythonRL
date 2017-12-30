from classes import *
import random
import threading
import time

def random_game_player(game, player):
    while game.gamestate == GameState.ONGOING:
        if game.current_player() == player:
            state = game.get_state(player)
            toilet, pile, hand = state[0], state[1], state[2:]

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

def main(players):
    game = Game(players)
    threads = []
    for player in players:
        t = threading.Thread(target=random_game_player, args=(game, player))
        t.start()

    try:
        while game.gamestate != GameState.FINISHED:
            pass
    except KeyboardInterrupt:
        game.gamestate = GameState.CRASHED
    finally:
        game.logger.write()

def prompt_players():
    # NOTE: Let the state be signified as an array such that the first element is the
    # current toilet number, the second element is the current pile number, and the
    # rest is the current hand. So the cardcount can be found by doing s[2:].

    jesse = Player('Jesse', 0, PlayerType.COMPUTER)
    nat = Player('Nat', 1, PlayerType.COMPUTER)
    alex = Player('Alex', 2, PlayerType.COMPUTER)
    john = Player('John', 3, PlayerType.COMPUTER)
    return [jesse, nat, alex, john]
    # return [jesse, nat]

if __name__ == '__main__':
    # for i in range(100):
        players = prompt_players()
        main(players)
        time.sleep(1)
