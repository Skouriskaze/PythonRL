from Tkinter import *
import random

class Color:
    '''
    A class to hold colors
    '''
    black = '#000000'
    gray = '#888888'
    red = '#ff0000'
    green = '#00ff00'
    blue = '#0000ff'

class Snake:
    '''
    A snake game.
    '''

    '''
    These are the actions the snake can take.
    The NOOP is to create a new game.
    DMAP maps actions to respective dx and dy.
    '''
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    NOOP = -1
    ACTIONS = [NOOP, LEFT, UP, RIGHT, DOWN]
    DMAP = {}
    DMAP[LEFT] = (-1, 0)
    DMAP[UP] = (0, -1)
    DMAP[RIGHT] = (1, 0)
    DMAP[DOWN] = (0, 1)
    DMAP[NOOP] = (0, 0)

    def __init__(self, width, height):
        ''' Create a snake game with set width and height '''
        self.width = width 
        self.height = height
        self.newGame()

        self.rects = []
 
    def newGame(self): 
        ''' Setting a game up. ''' 
        self.length = 1
        self.snake = [(self.height / 2, self.width / 2)]
        self.snake = [self.genApple()]
        self.apple = self.genApple()

        self.dx = 0
        self.dy = 0

        self.ongoing = True

    def genApple(self):
        ''' Just generates a random (x, y) pair. '''
        apple = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        return apple


    def move(self, action):
        ''' Sets the dx and dy of the snake, and then updates the game. '''
        dx, dy = Snake.DMAP[action]
        self.dx = dx
        self.dy = dy
        self.update()

    def transition(self):
        ''' Moves the snake. '''
        headx, heady = self.snake[-1]
        self.snake.append((headx + self.dx, heady + self.dy))

        while len(self.snake) > self.length:
            self.snake.pop(0)

    def submitMove(self, action):
        if self.ongoing:
            self.move(action)
            self.transition()
            self.update()
        else:
            self.newGame()


    def update(self):
        ''' Updates the game. Moves the snake and then checks for status changes
        like game over or picked up apple. '''
        # Check Collision
        if self.head() in self.snake[:-1]:
            self.ongoing = False
            return -10

        # Check Offscreen
        if self.head()[0] < 0 or \
                self.head()[1] < 0 or \
                self.head()[0] >= self.width or \
                self.head()[1] >= self.height:
                self.ongoing = False
                return -10

        # Check Apple
        if self.head() == self.apple:
            self.length += 1
            self.apple = self.genApple()
            return 10

        return 1

        
    def head(self):
        ''' Get the head of the snake '''
        return self.snake[-1]
    def body(self):
        return self.snake[:-1]


class Snake:
    '''
    A snake game.
    '''

    '''
    These are the actions the snake can take.
    The NOOP is to create a new game.
    DMAP maps actions to respective dx and dy.
    '''
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    NOOP = -1
    ACTIONS = [NOOP, LEFT, UP, RIGHT, DOWN]
    DMAP = {}
    DMAP[LEFT] = (-1, 0)
    DMAP[UP] = (0, -1)
    DMAP[RIGHT] = (1, 0)
    DMAP[DOWN] = (0, 1)
    DMAP[NOOP] = (0, 0)

    def __init__(self, width, height):
        ''' Create a snake game with set width and height '''
        self.width = width 
        self.height = height
        self.newGame()

        self.rects = []
 
    def newGame(self): 
        ''' Setting a game up. ''' 
        self.length = 1
        self.snake = [(self.height / 2, self.width / 2)]
        self.snake = [self.genApple()]
        self.apple = self.genApple()

        self.dx = 0
        self.dy = 0

        self.ongoing = True

    def genApple(self):
        ''' Just generates a random (x, y) pair. '''
        apple = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        return apple


    def update(self):
        ''' Updates the game. Moves the snake and then checks for status changes
        like game over or picked up apple. '''
        if self.ongoing:
            # Move
            self.transition()
            
            # Check Collision
            if self.head() in self.snake[:-1]:
                self.ongoing = False
                return False

            # Check Offscreen
            if self.head()[0] < 0 or self.head()[1] < 0 or self.head()[0] >= self.width or self.head()[1] >= self.height:
                    self.ongoing = False
                    return False

            # Check Apple
            if self.head() == self.apple:
                self.length += 1
                self.apple = self.genApple()
            return True
        else:
            if self.dx == 0 and self.dy == 0:
                self.newGame()

    def head(self):
        ''' Get the head of the snake '''
        return self.snake[-1]

    def move(self, action):
        ''' Sets the dx and dy of the snake, and then updates the game. '''
        dx, dy = Snake.DMAP[action]
        self.dx = dx
        self.dy = dy
        self.update()

    def transition(self):
        ''' Moves the snake. '''
        headx, heady = self.snake[-1]
        self.snake.append((headx + self.dx, heady + self.dy))

        while len(self.snake) > self.length:
            self.snake.pop(0)


class App:
    ''' The GUI of the game '''

    FPS = 12 # Frames per second
    SPF = 1000 / FPS
    PADDING = 2 # Padding between grid spaces

    def __init__(self, game=None, queue=[Snake.NOOP]):
        ''' Creates the window and snake game. '''
        self.root = Tk()
        self.width = 300
        self.height = 300
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.drawn = dict()

        if game == None:
            self.tilewidth = 10
            self.tileheight = 10
            self.game = Snake(self.tilewidth, self.tileheight)
        else:
            self.tilewidth = game.width
            self.tileheight = game.height
            self.game = game

        self.head = self.game.head()
        self.root.bind("<KeyPress>", self._keydown)

        self.queuemove = queue

    def _keydown(self, e):
        ''' Keyboard event handler. '''
        if e.keycode == 113 or e.keycode == 37:
            self.queuemove.append(Snake.LEFT)
            # self.game.move(Snake.LEFT)
        elif e.keycode == 114 or e.keycode == 39:
            self.queuemove.append(Snake.RIGHT)
            # self.game.move(Snake.RIGHT)
        elif e.keycode == 111 or e.keycode == 38:
            self.queuemove.append(Snake.UP)
            # self.game.move(Snake.UP)
        elif e.keycode == 116 or e.keycode == 40:
            self.queuemove.append(Snake.DOWN)
            # self.game.move(Snake.DOWN)

        elif e.keycode == 65:
            if not self.game.ongoing:
                self.game.newGame()
                self.queuemove.append(Snake.NOOP)

    def loop(self):
        ''' Updates and renders the snake game. '''
        # Grabbing move from queue
        if len(self.queuemove) > 0:
            self.game.move(self.queuemove.pop(0))

        # Updating
        # Rendering
        self.drawSnake()

        self.drawPoint(self.game.apple[0], self.game.apple[1], Color.red)
            
        # Resetting
        self.root.after(App.SPF, self.loop)


    def start(self):
        ''' Sets the update loop and starts the window '''
        self.root.after(App.SPF, self.loop)
        self.root.mainloop()
        

    def getCoords(self, x, y):
        ''' Get drawing coordinates of a grid point '''
        tilewidth = self.width / self.tilewidth
        tileheight = self.height / self.tileheight
        return (tilewidth * x + App.PADDING,
                tileheight * y + App.PADDING,
                tilewidth * (x + 1) - App.PADDING,
                tilewidth * (y + 1) - App.PADDING)

    def drawHead(self):
        self.head = self.game.head()
        self.drawPoint(self.head[0], self.head[1], Color.gray)

    def drawSnake(self):
        toDelete = [self.head]
        for x, y in self.drawn:
            if (x, y) not in self.game.snake[:-1]:
                toDelete.append((x, y))
        for space in toDelete:
            if space in self.drawn:
                self.canvas.delete(self.drawn[space])
                del(self.drawn[space])

        for x, y in self.game.snake[:-1]:
            if (x, y) not in self.drawn:
                self.drawPoint(x, y, Color.black)

        self.drawHead()

    
    def drawPoint(self, coordx, coordy, color):
        ''' Draws a grid point '''
        x, y, endx, endy = self.getCoords(coordx, coordy)
        rect = self.canvas.create_rectangle( x, y, endx, endy, fill=color)
        self.drawn[(coordx, coordy)] = rect
        return rect


if __name__ == '__main__':
    app = App()
    app.start()
