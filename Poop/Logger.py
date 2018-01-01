# TODO: Make a better, more consistent logger that includes toilet, pile, and card
# count

class Logger:
    ''' A logger. Use Logger.write() when the game ends to write a log. '''

    def __init__(self, filename, game):
        ''' Sets the filename of a logger '''
        self.filename = filename
        self.history = ""
        self.move_history = dict()
        self.game = game
        for player in game.players:
            self.move_history[player] = []

    def add_move(self, player, card, state):
        ''' Adds a move to the history '''
        self.history += "{} played {}. {} cards remaining.\n".format(player, card,
                len(player.deck.cardlist))

        self.move_history[player].append((state, card.index()))

    def add_flush(self, player):
        ''' Adds a flush to the history '''
        self.history += "{} flushed the toilet.\n".format(player)

    def add_clog(self, player):
        ''' Adds a clog to the history '''
        self.history += "{} clogged the toilet.\n".format(player)

    def add_draw(self, player, card):
        ''' Adds a player draw to the history '''
        self.history += "{} drew {}. {} cards remaining.\n".format(player, card,
                len(player.deck.cardlist))

    def add_toilet(self, toilet):
        ''' Adds a toilet draw to the history '''
        self.history += "A new toilet was drawn: {}.\n".format(toilet)

    def add_win(self, player):
        ''' Adds a win to the history '''
        self.history += "{} won the game.\n".format(player)
        for p in self.game.players:
            state = self.game.get_state(p)
            self.move_history[p].append((state, -1))

    def add_blank(self):
        ''' Adds a blank line to the history '''
        self.history += "\n"

    def add_custom(self, msg):
        ''' Adds a custom message to the history '''
        self.history += msg + "\n"

    def write(self):
        ''' Writes the history to the file '''
        with open("logs/{}.txt".format(self.filename), 'w') as f:
            f.write(self.history)

        for player in self.move_history:
            with open("logs/{}-{}.log".format(self.filename, player), 'w') as f:
                for state, move in self.move_history[player]:
                    f.write("{}|{}\n".format(state, move))

