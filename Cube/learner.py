import random
from cube import CubeWrapper, Cube

class SARSA:
    def __init__(self, wrapper, alpha=1, gamma=0.95):
        self.game = wrapper
        self.qvalues = dict()

    def getOptimal(self, state):
        # TODO: Move this if down into
        if state not in self.qvalues:
            if len(self.qvalues) == 0:
                self.qvalues[state] = 0
            else:
                nearest = (999999, 0)
                for k in self.qvalues:
                    nearest = min(nearest, (CubeWrapper.stateDifference(state, k),
                        self.qvalues[k]))

        best = (-999999, None)
        for action in Cube.MOVES:
            neighbor = self.game.pollState(action)
            best = max(best, (self.qvalues[neighbor], action))

        return best


    def getRandom(self, state):
        return random.choice(Cube.MOVES)

    def iterate(self, epsilon = 0.5):
        state = self.game.getState()
        if random.random() < epsilon:
            action = self.getRandom(state)
        else:
            action = self.getOptimal(state)

        reward = self.game.move(action)
        self.update(state, action)

    def update(self, state, action, reward):
        # TODO: Finish this
        self.qvalues[state] = self.qvalues[state] + alpha * (reward + gamma * 
