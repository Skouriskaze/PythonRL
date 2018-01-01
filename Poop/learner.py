import numpy as np
import tensorflow as tf
from classes import *
from util import convert_to_2d

class Network:
    IN_LAYER = Card.TOTAL_CARDS + 3
    HIDDEN_LAYER_1 = IN_LAYER + 2
    OUT_LAYER = Card.TOTAL_CARDS

    GAMMA = 0.95
    INITIAL_RANDOM = 0.25
    # NUM_EPISODES = 10000

    def __init__(self, checkpoint=None):
        self.nextQ = tf.placeholder(shape=[1, Network.OUT_LAYER], dtype=tf.float32)

        self.in_layer = tf.placeholder(shape=[1, Network.IN_LAYER], dtype=tf.float32)
        self.w1 = tf.get_variable("w1", shape=[Network.IN_LAYER, Network.OUT_LAYER],
                initializer=tf.constant_initializer(0.5))
        # self.w1 = tf.get_variable("w1", shape=[Network.IN_LAYER, Network.HIDDEN_LAYER_1],
                # initializer=tf.constant_initializer(0.5))
                # initializer=tf.random_uniform_initializer(0, 1))
        # self.hidden_layer = tf.nn.sigmoid(tf.matmul(self.in_layer, self.w1))

        # self.w2 = tf.get_variable("w2", shape=[Network.HIDDEN_LAYER_1, Network.OUT_LAYER],
                # initializer=tf.constant_initializer(0.5))
                # initializer=tf.random_uniform_initializer(0, 1))
        # self.output = tf.matmul(self.hidden_layer, self.w2)
        # self.output = tf.nn.sigmoid(self.output)
        self.output = tf.matmul(self.in_layer, self.w1)
        self.output = tf.nn.sigmoid(self.output)

        self.prediction = tf.argmax(self.output, 1)
        self.epsilon = Network.INITIAL_RANDOM

        self.loss = tf.reduce_sum(tf.square(self.nextQ - self.output))
        self.trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
        self.training_step = self.trainer.minimize(self.loss)

        self.saver = tf.train.Saver()

        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

        if checkpoint:
            self.saver.restore(self.sess, checkpoint)
            print("Checkpoint restored.")


    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_tb):
        self.close()

    def get_best_move(self, state):
        state = convert_to_2d(state)
        best, output = self.sess.run([self.prediction, self.output],
                feed_dict={self.in_layer: state})
        return best[0], output

    def get_train_move(self, state):

        # TODO: Consider making this smarter: only choose viable options??? It's not
        # cheating, it's called taking advantage of knowing the problem space
        best = self.get_best_move(state)

        if np.random.rand(1) < self.epsilon:
            best = np.random.randint(Network.OUT_LAYER)

        return best

    def get_q_value(self, next_state, reward):
        next_state = convert_to_2d(next_state)
        output = self.sess.run(self.output, feed_dict={self.in_layer: next_state})
        q = reward + self.GAMMA * np.max(output)
        return reward + self.GAMMA * np.max(output)

    def get_reward(self, state):
        ''' If you win, you get 100 reward. If you lose, you get -100 reward. Otherwise,
        -1 reward to promote winning faster '''
        state = convert_to_2d(state)
        if sum(state[0, 3:]) == 0:
            return 10
        elif state[0, 2] == 0:
            return -10

        return 0

    def train_step(self, state, move, next_state):
        state = convert_to_2d(state)
        next_state = convert_to_2d(next_state)
        q = self.get_q_value(next_state, self.get_reward(next_state))
        output = self.sess.run(self.output, feed_dict={self.in_layer: state})
        output[0, move] = q
        self.sess.run(self.training_step, feed_dict={self.in_layer: state, self.nextQ: output})

    def train_manual(self, state, move, q):
        state = convert_to_2d(state)
        output = self.sess.run(self.output, feed_dict={self.in_layer: state})
        output[0, move] = q
        self.sess.run(self.training_step, feed_dict={self.in_layer: state, self.nextQ: output})

    def close(self):
        self.sess.close()

    def save(self, path):
        self.saver.save(self.sess, "models/{}/weights.ckpt".format(path))

