

class Cube:
    def __init__(self):
        TODO: Get rid of the crap design
        self.U = [0 for x in range(4)]
        self.D = [1 for x in range(4)]
        self.L = [2 for x in range(4)]
        self.R = [3 for x in range(4)]
        self.F = [4 for x in range(4)]
        self.B = [5 for x in range(4)]

    def getLayer(self, layer):
        layer = layer.upper()
        return eval('self.' + layer)

    def getLeft(self, layer):
        if layer.lower() == 'f':
            pass

    def turnU(self):
        self.U = self.U[1:] + self.U[:1]
        swap = self.F[:2]
        self.F = self.R[:2] + self.F[2:]
        self.L = self.F[:2] + self.L[2:]
        self.B = self.R[:2] + self.F[2:]
        self.R = self.R[:2] + self.F[2:]


if __name__ == '__main__':
    c = Cube()
    for l in ['u', 'd', 'l', 'r', 'f', 'b']:
        print "%s: %s" % (l, c.getLayer(l))
