from learner import *
# from network import *
from util import parse_log_file
from classes import *

import glob
import sys
import random

def main():
    train_dir('logs/', 100, new_model=True)

def train(net, train_file):
    history = parse_log_file(train_file)
    assert len(history) > 1

    curr_idx = 0
    while curr_idx + 1 < len(history):
        # Train step
        # TODO: We need to think abotu this. We assume for the file given, the player
        # plays the "best" move, which might not be right. This is okay at first, but
        # we definitely will need a better ai...

        # It is still worth seeing what a RL agent can learn from a random agent. It
        # will still get rewards, so being close to winning should have a positive
        # q-value, but the further it gets, the higher chance it has of missing a good
        # move.

        curr_state, curr_move = history[curr_idx]
        next_state, next_move = history[curr_idx + 1]

        net.train_step(curr_state, curr_move, next_state)
        curr_idx += 1


def get_random_state():
    toilet = random.randint(Toilet.TOILET_MIN, Toilet.TOILET_MAX - 1)
    pile = random.randint(0, toilet - 1)
    lowest = random.randint(1, 5)
    num_cards = random.randint(1, 10)
    hand = [0 for _ in range(Card.TOTAL_CARDS)]
    for _ in range(num_cards):
        hand[random.randint(0, len(hand) - 1)] += 1

    return [toilet] + [pile] + [lowest] + hand

def train_legal_moves(num_iter):
    # "models/move_training/weights.ckpt"
    with Network() as net:
        for i in range(num_iter):
            state = get_random_state()
            hand = state[3:]
            # move, _ = net.get_best_move(state)
            # viable = []
            # nonviable = []
            # for j in range(len(hand)):
                # if hand[j] > 0:
                    # viable.append(j)
                # else:
                    # nonviable.append(j)

            # good = random.choice(viable)
            # bad = random.choice(nonviable)

            # net.train_manual(state, bad, 0)
            # net.train_manual(state, good, 1)

            move = random.randint(0, len(hand) - 1)
            if hand[move] > 0:
                net.train_manual(state, move, 0.8)
            else:
                net.train_manual(state, move, 0)
            
            sys.stdout.write("{:05}/{:05}\r".format(i, num_iter))

            if i % 1000 == 999:
                net.save("move_training")

        net.save("move_training")
        print("Network saved!")



def train_dir(directory, num_times, new_model=False):
    if directory[-1] != '/':
        directory += '/'

    files = glob.glob("{}*.log".format(directory))
    l = len(files)

    with Network("models/random_training/weights.ckpt" if not new_model else None) as net:
        for i in range(num_times):
            count = 0
            for f in files:
                count += 1
                train(net, f)
                sys.stdout.write("{:03}/{:03}: {:05}/{:05}\r".format(i, num_times, count, l))
            net.save("random_training")


if __name__ == '__main__':
    # main()
    train_legal_moves(50000)
