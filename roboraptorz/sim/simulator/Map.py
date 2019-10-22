import logging
import Robot
import copy
from matrix import Matrix

logger = logging.getLogger(__name__)

class Connection(object):
    def __init__(self, start, direction, color="B"):
        if direction[0][0] < 0 or direction[1][0] < 0 :
            self.start = start + direction
            self.direction = Matrix._makeMatrix([[0], [0]])
            self.direction[0][0] = -direction[0][0]
            self.direction[1][0] = -direction[1][0]
        else:
            self.start = start
            self.direction = direction
        self.color = color

    def __str__(self):
        return "[%i,%i] --> [%i,%i]" % (self.start[0][0], self.start[1][0], self.start[0][0] + self.direction[0], self.start[1][0] + self.direction[1][0])

    def __eq__(self, other):
        return self.start == other.start and self.direction == other.direction

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return int(self.start[0][0] + 100*self.start[1][0] + 10000*self.direction[0][0] + 1000000*self.direction[1][0])

class Map(object):
    def __init__(self):
        self.robots = []
        self.connections = []

    def loadMap(self, fileName):
        tempSet = set()
        with open(fileName, 'r') as fd:
            lines = fd.readlines()
            for m, line in enumerate(lines):
                for n, char in enumerate(line):
                    v1 = Matrix._makeMatrix([[m/3],[n/3]])
                    if char == '+' or char == '^' or char == '<' or char == 'v' or char == '>':
                        if (n + 1) < len(line):
                            v2 = Matrix._makeMatrix([[0], [1]])
                            if line[n+1] == '-':
                                tempSet.add(Connection(v1, v2))
                            elif line[n+1] == '=':
                                tempSet.add(Connection(v1, v2, "R"))
                        if (m + 1) < len(lines):
                            v2 = Matrix._makeMatrix([[1], [0]])
                            if lines[m+1][n] == '|':
                                tempSet.add(Connection(v1, v2))
                            elif lines[m+1][n] == '=':
                                tempSet.add(Connection(v1, v2, "R"))

                        # check for connections
                        if not char == '+':
                            self.registerRobot(copy.deepcopy(v1), char)
        self.connections = list(tempSet)

    def draw(self, edgeLength=3):
        # create data list
        xmax = 0
        ymax = 0
        for c in self.connections:
            if c.start[0][0] > xmax:
                xmax = int(c.start[0][0])
            if c.start[1][0] > ymax:
                ymax = int(c.start[1][0])

        data = [ [' ']*(ymax*edgeLength+1) for i in range(xmax*edgeLength +1)]

        # add connections
        for c in self.connections:
            start_x = int(c.start[0][0] * edgeLength)
            start_y = int(c.start[1][0] * edgeLength)
            end = c.start + c.direction
            end_x = int(end[0][0] * edgeLength)
            end_y = int(end[1][0] * edgeLength)
            data[start_x][start_y] = '+'
            for i in range(start_x, end_x):
                data[i+1][start_y] = '|'
            for i in range(start_y, end_y):
                data[start_x][i+1] = '-'
            data[end_x][end_y] = '+'

        # add robot
        for robot in self.robots:
            r_x = int(robot.globalPosition[0][0]) * edgeLength
            r_y = int(robot.globalPosition[1][0]) * edgeLength
            data[r_x][r_y] = 'o'

        for line in data:
            print(''.join(line))

    def getRobots(self):
        return self.robots

    def registerRobot(self, position, orientationAscii):
        rotLocToGlob = Matrix._makeMatrix([[1, 0], [0, 1]])
        rotGlobToLoc = Matrix._makeMatrix([[1, 0], [0, 1]])
        if orientationAscii == '^':
            rotLocToGlob = Matrix._makeMatrix([[1, 0], [0, 1]])
            rotGlobToLoc = Matrix._makeMatrix([[1, 0], [0, 1]])
        elif orientationAscii == '<':
            rotLocToGlob = Matrix._makeMatrix([[0, 1], [-1, 0]])
            rotGlobToLoc = Matrix._makeMatrix([[0, -1], [1, 0]])

        elif orientationAscii == 'v':
            rotLocToGlob = Matrix._makeMatrix([[-1, 0], [0, -1]])
            rotGlobToLoc = Matrix._makeMatrix([[-1, 0], [0, -1]])
        elif orientationAscii == '>':
            rotLocToGlob = Matrix._makeMatrix([[0, -1], [1, 0]])
            rotGlobToLoc = Matrix._makeMatrix([[0, 1], [-1, 0]])

        self.robots.append(Robot.Robot(self, position, rotLocToGlob, rotGlobToLoc))

    def getColor(self, fromGlobal, directionGlobal):
        c = Connection(fromGlobal, directionGlobal)

        try:
            index = self.connections.index(c)
        except:
            return ""
        else:
            return self.connections[index].color

    def isConnection(self, fromGlobal, directionGlobal):
        c = Connection(fromGlobal, directionGlobal)

        if c in self.connections:
            return True
        return False


if __name__ == "__main__":
    map = Map()
    map.loadMap("default.map")
    map.draw()
    r = map.getRobots()[0]

    print(r.globalPosition)
    print(r.scan())
    vlocal = Matrix._makeMatrix([[-1], [0]])
    map.draw()
    r.moveLocal(vlocal)
    map.draw()
    print(r.globalPosition)
    print(r.scan())
    r.moveLocal(vlocal)
    map.draw()
    print(r.globalPosition)
    print(r.scan())

