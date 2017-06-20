import random
from Tkinter import *

class Color:
    '''
    A class to hold colors
    '''
    black = '#000000'
    gray = '#888888'
    red = '#ff0000'
    green = '#00ff00'
    blue = '#0000ff'


class Tetris:
    LPIECE = 0
    OPIECE = 1
    PIECES = [LPIECE, OPIECE]

    def __init__(self, width=7, height=7):
        self.width = width;
        self.height = height

        self.newGame()

    def newGame(self):
        self.currentPiece = random.choice(Tetris.PIECES)
        # self.grid = [[None for x in range(self.height)] for y in range(self.width)]
        self.state = [0 for x in range(self.width)]

    def move(self, location):
        self.placePiece(self.currentPiece, location)
        self.currentPiece = random.choice(Tetris.PIECES)

    def placePiece(self, piece, location):
        if piece == Tetris.LPIECE:
            self.state[location] += 2
        elif piece == Teteris.OPIECE:
            self.state[location] += 1
            self.state[location + 1] += 1

class App:
    ''' The GUI of the game '''

    FPS = 12 # Frames per second
    SPF = 1000 / FPS
    PADDING = 2 # Padding between grid spaces

    def __init__(self, game=None):
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
            self.game = Tetris(self.tilewidth, self.tileheight)
        else:
            self.game = game
            self.tilewidth = game.width
            self.tileheight = game.height


        self.location = self.width // 2
        self.grid = [[None for j in range(self.tileheight)] for i in range(self.tilewidth)]

        self.root.bind("<KeyPress>", self._keydown)

    def _keydown(self, e):
        ''' Keyboard event handler. '''
        if e.keycode == 113 or e.keycode == 37:
            self.location -= 1
            self.location = max(self.location, 0)
        elif e.keycode == 114 or e.keycode == 39:
            self.location += 1
            self.location = min(self.location, self.width - 1)
        elif e.keycode == 116 or e.keycode == 40:
            self.game.move(self.location)

        elif e.keycode == 65:
            if not self.game.ongoing:
                self.game.newGame()

    def loop(self):
        ''' Updates and renders the snake game. '''
        # Updating
        # Rendering
        self.canvas.delete('all')
        
        for loc, height in zip(range(len(self.game.state)), self.game.state):
            for i in range(height):
                drawPoint(loc, i, Color.black)

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

    
    def drawPoint(self, coordx, coordy, color):
        ''' Draws a grid point '''
        x, y, endx, endy = self.getCoords(coordx, coordy)
        rect = self.canvas.create_rectangle( x, y, endx, endy, fill=color)
        self.drawn[(coordx, coordy)] = rect
        return rect

if __name__ == '__main__':
    t = Tetris()
    app = App(t)
    app.start()