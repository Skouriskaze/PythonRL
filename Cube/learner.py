import random
import time
import sys
from cube import CubeWrapper, Cube

class SARSA:
    def __init__(self, wrapper, alpha=1, gamma=0.95):
        self.game = wrapper
        self.qvalues = dict()
        self.alpha = alpha
        self.gamma = gamma

        try:
            self.loadQ()
        except:
            print "No q file"

    def learn(self, iterations, epsilon=0.5):
        for i in range(iterations):
            if i % 100 == 0 and i > 0:
                with open('qvalues.txt', 'w') as f:
                    f.write(str(self.qvalues))

        self.saveQ()

    def saveQ(self):
        with open('qvalues.txt', 'w') as f:
            f.write(str(self.qvalues))

    def loadQ(self):
        with open('qvalues.txt') as f:
            self.qvalues = eval(f.read())


    def getOptimal(self, state):
        best = (-999999, None)
        for action in Cube.MOVES:
            neighbor = self.game.pollState(action)
            best = max(best, (self.getValue(neighbor), action))

        return best[1]


    def getRandom(self, state):
        # TODO: Make this better (cube)
        return random.choice(Cube.MOVES)

    def iterate(self, epsilon = 0.5):
        now = time.time()
        state = self.game.getState()
        if random.random() < epsilon:
            action = self.getRandom(state)
        else:
            action = self.getOptimal(state)
        first = time.time() - now
        now = time.time()

        self.update(state, action)
        return first, time.time() - now

    def update(self, state, action):
        statep, reward = self.game.move(action)
        self.qvalues[state] = self.getValue(state) + self.alpha * (reward + self.gamma *
                self.getValue(statep) - self.getValue(state))

    def getValue(self, state):
        if state not in self.qvalues:
            if len(self.qvalues) == 0:
                self.qvalues[state] = 0
            else:
                nearest = (999999, 0)
                for k in self.qvalues:
                    nearest = min(nearest, (CubeWrapper.stateDifference(state, k),
                        self.qvalues[k]))
                self.qvalues[state] = nearest[1]

        return self.qvalues[state]



if __name__ == '__main__':
    cw = CubeWrapper()
    cw.getInitState()

    learner = SARSA(cw)
    oldQ = learner.qvalues

    print "Started learning."
    start = time.time()
    learner.learn(100)
    newQ = learner.qvalues
    print "Ended learning, took %d time" % (time.time() - start)
