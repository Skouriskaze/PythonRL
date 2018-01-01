

def shuffle(a):
    import random
    for i in range(len(a))[::-1]:
        idx = random.randint(0, i)
        a[idx], a[i] = a[i], a[idx]



def parse_log_file(fin):
    history = []
    with open(fin) as f:
        for line in f:
            line = line.strip()
            state, move = line.split("|")
            state = eval(state)
            move = int(move)
            history.append((state, move))

    return history


def convert_to_2d(state):
    import numpy as np
    return np.reshape(state, (1, -1))


def prompt_players():
    from classes import Player, PlayerType
    # NOTE: Let the state be signified as an array such that the first element is the
    # current toilet number, the second element is the current pile number, the third
    # number is the lowest card count other than you, and the
    # rest is the current hand. So the cardcount can be found by doing s[3:].

    jesse = Player('Jesse', 0, PlayerType.COMPUTER)
    nat = Player('Nat', 1, PlayerType.COMPUTER)
    alex = Player('Alex', 2, PlayerType.COMPUTER)
    john = Player('John', 3, PlayerType.COMPUTER)
    return [jesse, nat, alex, john]
    # return [jesse, nat]

def create_games(num_games):
    import sys
    for i in range(num_games):
        players = prompt_players()
        play_game(players, "{:04}".format(i + 1))
        sys.stdout.write("{:04} / {:04}\r".format(i + 1, num_games))
