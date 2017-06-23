from snake import App, Snake
import random
import threading
import time
import sys
import heapq


# TODO: Save in a file?
class QLearner:
    # Bellman Eq
    # Q(state, action) = R(state, action) + Gamma * Max[Q(next state, all actions)]
    def __init__(self, game, alpha=0.1, gamma=0.95, epsilon=0.8):
        self.game = game
        self.qvalue = dict()

        # Learning rate
        self.alpha = alpha
        # Gamma
        self.gamma = gamma
        # Epsilon
        self.epsilon = epsilon

        self.iteration = 0

    def initQvalue(self):
        pass

    def get(self, state):
        if state not in self.qvalue:
            self.qvalue[state] = random.random() * 10
        return self.qvalue[state]

    def trainStep(self):
        state = self._getState(self.game)
        action = self.getTrainMove(state)
        reward, result = self.game.submitMove(action)
        
        self.qvalue[state] = reward + self.gamma * self.get(result)

        self.iteration += 1
        sys.stdout.write("%d \r" % self.iteration)
        sys.stdout.flush()

    def getTrainMove(self, state):
        if self.game.ongoing:
            if random.random() < self.epsilon:
                # TODO: Maybe make it so you choose something that's not policy
                return Snake.randomAction()
            else:
                return getPolicyMove(self)
        else:
            return Snake.ACTIONS.NOOP

    def getPolicyMove(self, state):
        if self.game.ongoing:
            policyMove = (None, Snake.NOOP)
            for action in Snake.ACTIONS:
                newstate = self.game.pollAction(state, action)
                if not self.game.isEmpty(newstate):
                    policyMove = max(policyMove, (self.get[newstate], action))
            if policyMove[1] == Snake.NOOP:
                return Snake.randomAction()
            return policyMove
        else:
            return Snake.ACTIONS.NOOP

    def _getState(self):
        head = self.game.head()
        apple = self.game.apple

        return None


    def _saveQ(self, filepath='qvalues.txt'):
        with open(filepath, 'w') as f:
            f.write(self.qvalue)
    def loadQ(self, filepath='qvalues.txt'):
        with open(filepath, 'r') as f:
            qvalue = f.read()
        self.qvalue = eval(qvalue)

def main():
    class Info:
        ''' This class holds information that the thread can access. '''
        pass
    Info.ongoing = True # Whether we should continue sending moves.
    Info.snake = Snake(10, 10) # Snake game

    Info.score = 0
    def makeMove():
        '''  Thread that sends a move to the snake game '''
        while Info.ongoing:
            if Info.snake.ongoing:
                # If there are no moves queued, the snake game
                # is at the most updated state
                time.sleep(1 / 10.) # For some reason, sleeping it makes
                                 # the gui run faster
                action = astar()
                reward = Info.snake.submitMove(action)
                # sys.stdout.write('%s   \r' % (action))
                # sys.stdout.flush()
                # Info.score += reward
            else:
                # The game is over. Wait some time and then
                # reset the game
                time.sleep(1)
                Info.snake.submitMove(Snake.NOOP)
                Info.score = 0

    def trainQL():
        ''' Thread that learns '''
        ql = QLearner(Info.snake)
        for i in xrange(1000):
            ql.trainStep()
        runQL()
                    
                
    def runQL():
        pass
            
    def chooseMove():
        ''' Chooses a move. Naively heads to the horizontal coordinate,
        then the vertical coordinate. '''
        head = Info.snake.head()
        apple = Info.snake.apple
        if head[0] > apple[0]:
            return Snake.LEFT
        elif head[0] < apple[0]:
            return Snake.RIGHT
        else:
            if head[1] > apple[1]:
                return Snake.UP
            else:
                return Snake.DOWN

        return Snake.randomAction()

    def gbf():
        ''' Greedy Best First Search '''
        def dist((x1, y1), (x2, y2)):
            return abs(x1 - x2) + abs(y1 - y2)

        start = Info.snake.head()
        goal = Info.snake.apple
        best = (999999, None)
        for action in Snake.ACTIONS:
            neighbor = Info.snake.pollAction(start, action)
            if Info.snake.isEmpty(neighbor):
                best = min(best, (dist(neighbor, goal), action))


        if best[1] == None:
            return Snake.randomAction()

        return best[1]
    
    def astar():
        ''' A* Search '''
        def dist((x1, y1), (x2, y2)):
            return abs(x1 - x2) + abs(y1 - y2)

        start = Info.snake.head()
        goal = Info.snake.apple

        parents = dict()
        parents[start] = (Snake.NOOP, start)

        q = [(0, start)]
        while q:
            cost, curr = heapq.heappop(q)
            if curr == goal:
                # Find path, then return the first action
                action = gbf()
                while curr != start:
                    action, curr = parents[curr]
                return action

            # Adds neighbors to the queue
            for action in Snake.ACTIONS:
                neighbor = Info.snake.pollAction(curr, action)
                if Info.snake.isEmpty(neighbor) and \
                        (neighbor not in parents):
                    parents[neighbor] = (action, curr)
                    heapq.heappush(q, (dist(neighbor, goal), neighbor))

        # If A* cannot find a path, take the greedy best first action
        return gbf()
                


    app = App(game=Info.snake)
    thd = threading.Thread(name="Movemaker", target=makeMove)
    thd.daemon = True
    thd.start() 
    app.start()

    Info.ongoing = False


if __name__ == '__main__':
    main()
