import random

class Cubie:
    FACES = ['U', 'D', 'L', 'R', 'F', 'B']

    def __init__(self):
        self.faces = dict()
        for l in Cubie.FACES:
            self.faces[l] = None

    def getFace(self, face):
        if face not in Cubie.FACES:
            raise Exception('Face %s does not exist.' % face)

        return self.faces[face]

    def setFace(self, face, value):
        if face not in Cubie.FACES:
            raise Exception('Face %s does not exist.' % face)

        old = self.faces[face]
        self.faces[face] = value
        return old

    def rotate(self, pitch=0, roll=0, yaw=0):
        ''' rotate '''
        if pitch:
            pitch = 1 if pitch > 0 else -1
            path = 'BDFU'[::pitch]
            self._cycleFaces(path)

        if roll:
            roll = 1 if roll > 0 else -1
            path = 'LURD'[::roll]
            self._cycleFaces(path)

        if yaw:
            yaw = 1 if yaw > 0 else -1
            path = 'BRFL'[::yaw]
            self._cycleFaces(path)


    def _cycleFaces(self, faces):
        faces = list(faces)
        if len(faces) > 0:
            skip = self.getFace(faces[-1])
            for face in faces:
                skip = self.setFace(face, skip)

    def __str__(self):
        ret = ''

        ret += ' '  + str(self.getFace('U'))
        ret += '\n'
        ret += str(self.getFace('L')) + str(self.getFace('F')) + str(self.getFace('R')) + str(self.getFace('B'))
        ret += '\n'
        ret += ' '  + str(self.getFace('D'))

        return ret

class Cube:
    LAYERS = ['U', 'D', 'L', 'R', 'F', 'B']
    MOVES = [l for l in LAYERS] + [l + "'" for l in LAYERS]

    def __init__(self, state=None):
        if not state:
            self.resetCube()
        else:
            self.setCube(state)

        self._cubieIndices = dict()
        self._cubieIndices['U'] = [0, 1, 3, 2]
        self._cubieIndices['D'] = [5, 4, 6, 7]
        self._cubieIndices['L'] = [0, 2, 6, 4]
        self._cubieIndices['R'] = [3, 1, 5, 7]
        self._cubieIndices['F'] = [2, 3, 7, 6]
        self._cubieIndices['B'] = [1, 0, 4, 5]

    def scrambleCube(self, moves=1):
        actions = [random.choice(Cube.MOVES) for _ in range(moves)]
        for action in actions:
            self.turn(action)

    def setCube(self, state):
        if type(state) == str:
            state = eval(state)

        self.cubies = [Cubie() for _ in range(8)]

        for layer in Cube.LAYERS:
            for face, cubie in zip(state[:4], self.getLayer(layer)):
                cubie.setFace(layer, face)
            state = state[4:]

    def getLayer(self, layer):
        if layer not in Cube.LAYERS:
            raise Exception('Layer %s does not exist.' % layer)

        if layer.upper() == 'U':
            return self.cubies[:4]
        elif layer.upper() == 'D':
            return self.cubies[6:8] + self.cubies[4:6]

        elif layer.upper() == 'B':
            return self.cubies[0:1] + self.cubies[1:2] + self.cubies[4:5] + self.cubies[5:6]
        elif layer.upper() == 'F':
            return self.cubies[2:4] + self.cubies[6:8]

        elif layer.upper() == 'R':
            return self.cubies[3:4] + self.cubies[1:2] + self.cubies[7:8] + self.cubies[5:6]
        elif layer.upper() == 'L':
            return self.cubies[0:1] + self.cubies[2:3] + self.cubies[4:5] + self.cubies[6:7]

    def resetCube(self):
        self.cubies = [Cubie() for _ in range(8)]
        for i in range(len(Cube.LAYERS)):
            layer = Cube.LAYERS[i]
            for cubie in self.getLayer(layer):
                cubie.setFace(layer, i)

    def setCubie(self, index, value):
        old = self.cubies[index]
        self.cubies[index] = value
        return old

    def _cycleLayer(self, layer, prime=False):
        indices = self._cubieIndices[layer][::1 if not prime else -1]

        skip = self.cubies[indices[-1]]
        for index in indices:
            skip = self.setCubie(index, skip)

    def turn(self, move, prime=False):
        move = move.upper()
        if len(move) > 1:
            if move[1] == "'":
                prime = True
            move = move[0]

        for cubie in self.getLayer(move):
            if move == 'U':
                cubie.rotate(yaw=1 if not prime else -1)
            elif move == 'D':
                cubie.rotate(yaw=-1 if not prime else 1)
            elif move == 'L':
                cubie.rotate(pitch=-1 if not prime else 1)
            elif move == 'R':
                cubie.rotate(pitch=1 if not prime else -1)
            elif move == 'F':
                cubie.rotate(roll=1 if not prime else -1)
            elif move == 'B':
                cubie.rotate(roll=-1 if not prime else 1)
        self._cycleLayer(move, prime)

    def moveAlgorithm(self, alg):
        moves = self._parseAlgorithm(alg)
        for move in moves:
            self.turn(move)

    def _parseAlgorithm(self, alg):
        alg = alg.upper()
        moves = []
        current = ''
        index = 0
        while index < len(alg):
            if current + alg[index] in Cube.MOVES:
                current += alg[index]
            else:
                if current in Cube.MOVES:
                    moves.append(current)
                current = alg[index]
            index += 1
        if current in Cube.MOVES:
            moves.append(current)

        return moves

    def isSolved(self):
        for layer in Cube.LAYERS:
            cubies = [cubie.getFace(layer) for cubie in self.getLayer(layer)]
            if not all([c == cubies[0] for c in cubies]):
                return False
        return True

    def toState(self):
        # TODO: Put this in another method
        state = []
        faces = dict()
        for layer in Cube.LAYERS:
            cubies = [cubie.getFace(layer) for cubie in self.getLayer(layer)]
            state += cubies
        return tuple(state)

    def __str__(self):
        ret = ''
        faces = dict()
        for layer in Cube.LAYERS:
            faces[layer] = [cubie.getFace(layer) for cubie in self.getLayer(layer)]
        
        ret += ' ' * 6
        ret += str(faces['U'][:2])
        ret += '\n'
        ret += ' ' * 6
        ret += str(faces['U'][2:])
        ret += '\n'


        ret += str(faces['L'][:2]) + str(faces['F'][:2]) + str(faces['R'][:2]) \
            + str(faces['B'][:2])
        ret += '\n'
        ret += str(faces['L'][2:]) + str(faces['F'][2:]) + str(faces['R'][2:]) \
            + str(faces['B'][2:])
        ret += '\n'

        ret += ' ' * 6
        ret += str(faces['D'][:2])
        ret += '\n'
        ret += ' ' * 6
        ret += str(faces['D'][2:])
        ret += '\n'
        return ret

class CubeWrapper:
    # TODO: Get better polling states, make cube constructor with a state
    def __init__(self, cube=None):
        if cube:
            self.cube = cube
        else:
            self.cube = Cube()

    def getInitState(self):
        self.cube.scrambleCube()

    def getState(self, cube=None):
        if not cube:
            cube = self.cube
        return cube.toState()

    def _getOpposite(self, move):
        move = move.upper()
        idx = Cube.MOVES.index(move)
        return Cube.MOVES[idx - len(Cube.MOVES) / 2]

    def pollState(self, move, cube=None):
        if not cube:
            cube = self.cube

        cube.turn(move)
        state = self.getState(cube)
        cube.turn(self._getOpposite(move))
        return state

    def isStateSolved(self, state=None):
        if not state:
            state = self.getState()

        assert len(state) % 4 == 0
        while state:
            temp = state[:4]
            if not all([c == temp[0] for c in temp]):
                return False
            state = state[4:]

        return True

    def move(self, move):
        state = self.getState()
        if self.isStateSolved(state):
            # TODO: rename scramble
            self.game.scrambleCube()
            statep = self.getState()
        else:
            self.cube.turn(move)
            statep = self.getState()

        return statep, self.reward(state, move, statep)

    def reward(self, state, move, statep):
        if self.isStateSolved(statep):
            return 100
        else:
            return -1

    @staticmethod
    def stateDifference(s1, s2):
        diff = 0
        assert len(s1) == len(s2)
        for a, b in zip(s1, s2):
            diff += abs(a - b)
        return diff


if __name__ == '__main__':
    c = Cube()
    c.moveAlgorithm("r")
    print c
    s = c

    c = Cube(s)
    print c


    # c.moveAlgorithm("rl' ud' fb'")
    # print c
    # print c.isSolved()
    # cw = CubeWrapper(c)

    # from learner import SARSA
    
