from snake import App, RLSnake as Snake
import random
import threading
import time
import sys
import heapq

# TODO: RL to play Snake
# TODO: A* smart to play Snake



class QLearner:
    def __init__(self, game):
        self.game = game
        self.qvalue = dict()

        # Learning rate
        self.alpha = 0.1
        # Gamma
        self.gamma = 0.95
        # Epsilon
        self.epsilon = 0.8

    def getTrainMove(self, state):
        if random.random() < self.epsilon:
            # TODO: Maybe make it so you choose something that's not policy
            return Snake.randomAction()
        else:
            return getPolicyMove(self)

    def getPolicyMove(self, state):
        policyMove = (None, Snake.NOOP)
        for action in Snake.ACTIONS:
            newstate = self.game.pollAction(state, action)
            if self.game.isEmpty(newstate):
                policyMove = max(policyMove, (self.qvalue[newstate], action))
        return policyMove


def main():
    class Info:
        ''' This class holds information that the thread can access. '''
        pass
    Info.ongoing = True # Whether we should continue sending moves.
    Info.snake = Snake(8, 8) # Snake game

    Info.score = 0
    def makeMove():
        '''  Thread that sends a move to the snake game '''
        while Info.ongoing:
            if Info.snake.ongoing:
                if len(Info.snake.movequeue) == 0:
                    # If there are no moves queued, the snake game
                    # is at the most updated state
                    time.sleep(1 / 10.) # For some reason, sleeping it makes
                                     # the gui run faster
                    reward = Info.snake.submitMove(astar())
                    sys.stdout.write('%d (+%d)    \r' % (Info.score, reward))
                    sys.stdout.flush()
                    Info.score += reward
            else:
                # The game is over. Wait some time and then
                # reset the game
                time.sleep(1)
                Info.snake.newGame()
                Info.score = 0
                    
                
            
    def chooseMove():
        ''' Chooses a move. Naively heads to the horizontal coordinate,
        then the vertical coordinate. '''
        head = Info.snake.head
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

        start = Info.snake.head
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

        start = Info.snake.head
        goal = Info.snake.apple

        parents = dict()
        parents[start] = (Snake.NOOP, start)
        costs = dict()
        costs[start] = 0

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
                        (neighbor not in costs or costs[neighbor] > cost + 1):
                    parents[neighbor] = (action, curr)
                    costs[neighbor] = cost + 1
                    heapq.heappush(q, (dist(neighbor, goal) + cost + 1, neighbor))

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