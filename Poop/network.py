import random
import sys
import tensorflow as tf
import numpy as np

class Network:
    def __init__(self, checkpoint=None):
        self.nextQ = tf.placeholder(shape=[1, 18], dtype=tf.float32)

        self.in_layer = tf.placeholder(shape=[1, 21], dtype=tf.float32)
        self.w1 = tf.get_variable("w1", shape=[21, 18],
                initializer=tf.constant_initializer(0.5))
        self.output = tf.matmul(self.in_layer, self.w1)
        self.output = tf.nn.sigmoid(self.output)

        self.prediction = tf.argmax(self.output, 1)

        self.loss = tf.reduce_sum(tf.square(self.nextQ - self.output))
        self.trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
        self.training_step = self.trainer.minimize(self.loss)

        self.saver = tf.train.Saver()

        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

        if checkpoint:
            self.saver.restore(self.sess, checkpoint)
            print("Checkpoint restored.")


    def get_best_move(self, state):
        state = conv(state)
        best, output = self.sess.run([self.prediction, self.output],
                feed_dict={self.in_layer: state})
        return best[0], output

    def train_manual(self, state, move, q):
        state = conv(state)
        output = self.sess.run(self.output, feed_dict={self.in_layer: state})
        output[0, move] = q
        self.sess.run(self.training_step, feed_dict={self.in_layer: state, self.nextQ: output})


    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_tb):
        self.close()

    def close(self):
        self.sess.close()

    def save(self, path):
        self.saver.save(self.sess, "models/{}/weights.ckpt".format(path))


def conv(state):
    return np.reshape(state, (1, -1))

def get_state():
    toilet = random.randint(8, 14)
    pile = random.randint(0, toilet - 1)
    lowest = random.randint(1, 5)
    num_cards = random.randint(1, 10)
    hand = [0 for _ in range(18)]
    for _ in range(num_cards):
        hand[random.randint(0, len(hand) - 1)] += 1

    return [toilet] + [pile] + [lowest] + hand

def train_network(net, num_iter):
    for i in range(num_iter):
        state = get_state()
        hand = state[3:]
        move = random.randint(0, len(hand) - 1)

        if hand[move] > 0:
            net.train_manual(state, move, 0.8)
        else:
        # if hand[move] == 0:
            net.train_manual(state, move, 0)

        sys.stdout.write("{:05}/{:05}\r".format(i, num_iter))

        if i % 1000 == 999:
            net.save("tester")

    net.save("tester")
    print("Done training!")


def test_network(net, num_test):
    total_good = 0
    for i in range(num_test):
        state = get_state()
        hand = state[3:]
        move, output = net.get_best_move(state)

        good = hand[move] > 0
        # if not good:
        print("State: {}".format(state))
        print("Best: {}".format(move))
        print("Output: {}".format(output))
        print(good)
        if good:
            total_good += 1
    print("{}/{}".format(total_good, num_test))

if __name__ == '__main__':
    with Network() as net:
        train_network(net, 50000)
        test_network(net, 100)
