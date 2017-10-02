from Tkinter import *

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

        if game == None:
            self.tilewidth = 10
            self.tileheight = 10
            self.game = CubeWrapper()
        else:
            self.tilewidth = game.width
            self.tileheight = game.height
            self.game = game

        self.root.bind("<KeyPress>", self._keydown)

    def _keydown(event):
        pass


    def loop(self):
        ''' Updates and renders the snake game. '''
            
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
        if (coordx, coordy) in self.drawn:
            self.canvas.delete(self.drawn[(coordx, coordy)])
        self.drawn[(coordx, coordy)] = rect
        return rect



    
