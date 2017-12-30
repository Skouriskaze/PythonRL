import numpy as np
import tensorflow as tf
from classes import *

class Network:
    IN_LAYER = Card.TOTAL_CARDS + 2
    HIDDEN_LAYER_1 = Network.IN_LAYER + 2
    OUT_LAYER = Card.TOTAL_CARDS

    GAMMA = 0.95
    INITIAL_RANDOM = 0.25
    # NUM_EPISODES = 10000

    def __init__(self):
        nextQ = tf.placeholder(shape=[1, Network.OUT_LAYER], dtype=tf.float32)

        self.in_layer = tf.placeholder(shape=[1, Network.IN_LAYER], dtype=tf.float32)
        self.w1 = tf.Variable(tf.random_uniform([Network.IN_LAYER, Network.HIDDEN_LAYER_1], 0, 0, 0.1))
        self.hidden_layer = tf.matmul(self.in_layer, self.w1)
        self.w2 = tf.Variable(tf.random_uniform([Network.HIDDEN_LAYER_1, Network.OUT_LAYER], 0, 0, 0.1))
        self.output = tf.matmul(self.hidden_layer, self.w2)

        self.prediction = tf.argmax(self.output, 1)
        self.epsilon = Network.INITAL_RANDOM

        
        loss = tf.reduce_sum(tf.square(nextQ - output))
        trainer = tf.train.GradientDescentOptimizer(learning_rate = 0.1)

        self.sess = tf.Session()
        sess.run(tf.initialize_all_variables())


    def get_train_move(self, state):
        best, output = sess.run([self.prediction, self.output],
                feed_dict={self.in_layer: state})

        if np.random.rand(1) < self.epsilon:
            best[0] = np.random.randint(Network.OUT_LAYER)

        return best[0]


    def train_step(self, state):
        pass

        
