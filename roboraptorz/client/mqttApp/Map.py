
import logging
import queue

from Common import *

logger = logging.getLogger(__name__)

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, roboDirection):
        dx = 0
        dy = 0
        if roboDirection == RoboDirection.NORTH:
            dx = 0;
            dy = 1;
        elif roboDirection == RoboDirection.EAST:
            dx = 1;
            dy = 0;
        elif roboDirection == RoboDirection.SOUTH:
            dx = 0;
            dy = -1;
        else:
            dx = -1;
            dy = 0;
        return Point(self.x + dx, self.y + dy)



    def __key(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class RelativeDirection:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def __key(self):
        return (self.dx, self.dy)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.dx == other.dx and self.dy == other.dy

class AvailableDirection:
    def __init__(self):
        self.direction = RoboDirection.NORTH
        self.explored = False
        self.distanceToUnexplored = -1

    def hasUnexploredChildren(self):
        if self.distanceToUnexplored == -1:
            return False
        return True

class Map:
    ROBOT_LOCATION_KEY = "robotLocation"
    START_POINT_KEY = "startPoint"
    SYNC_LINE_KEY = "syncLine"

    class MapNode:
        def __init__(self, coords):
            self.coord = coords
            self.isExplored = False
            self.availableDirections = []

        def addAvailableDirection(self, direction):
            if not(direction in self.availableDirections):
                self.availableDirections.append(direction)

    def __init__(self, mapName):
        initalLocation = Point(0,0)
        self._mapName = mapName
        self._roboLocation = initalLocation
        self.mapPoints = { initalLocation: self.MapNode(initalLocation)}
        self.pointsOfInterest = {}

    def addDirectionsAtCurrentLocation(self, directions):
        point = self.getRobotLocation()
        mapPoint = self.mapPoints[point]
        for direction in directions:
            logger.debug(self._mapName + ": setting connection from (" + str(point.x) + "," + str(point.y) + ") to (" + str(direction.dx) + "," + str(direction.dy) + ")")
            mapPoint.addAvailableDirection(direction)

    def setRobotLocation(self, point):
        logger.debug(self._mapName + ": setting robot location at (" + str(point.x) + "," + str(point.y) + ")")
        if not point in self.mapPoints:
            self.mapPoints[point] = self.MapNode(point)
        mapNode = self.mapPoints[point].isExplored = True
        self._roboLocation = point

    def getRobotLocation(self):
        return self._roboLocation

    def setStartPoint(self, point):
        logger.debug(self._mapName + ": setting start location at (" + str(point.x) + "," + str(point.y) + ")")
        self.pointsOfInterest[self.START_POINT_KEY] = point

    def setSyncLine(self, direction):
        p,d = direction
        logger.debug(self._mapName + ": setting sync line from (" + str(p.x) + "," + str(p.y) + ") to (" + str(d.dx) + "," + str(d.dy) + ")")
        self.pointsOfInterest[self.SYNC_LINE_KEY] = direction

    def getAvailableDirections(self):
        loc = self._roboLocation
        curentNode = self.mapPoints[loc]
        availableDirections = curentNode.availableDirections
        logger.debug("getAvailableDirec")
        result = []
        for dir in availableDirections:
            newPoint = Point(loc.x + dir.dx, loc.y + dir.dy)
            if newPoint in self.mapPoints:
                nextNode = self.mapPoints[newPoint]
                hasUnexploredChildren, distance = self._hasNodeUnexploredChildren(nextNode)
                availableDirection = AvailableDirection()
                availableDirection.direction = self.parseDirection(dir)
                availableDirection.explored = nextNode.isExplored
                availableDirection.distanceToUnexplored = distance
                result.append(availableDirection)
            else:
                availableDirection = AvailableDirection()
                availableDirection.direction = self.parseDirection(dir)
                availableDirection.explored = False
                availableDirection.distanceToUnexplored = 0
                result.append(availableDirection)
        return result

    def _hasNodeUnexploredChildren(self, node):
        distances = []
        hasUnexploredAncestor = False

        visitedPoints = []

        availablePoints = queue.Queue()
        availablePoints.put((node.coord,0))

        while not availablePoints.empty():
            currentPoint, dist = availablePoints.get()
            visitedPoints.append(currentPoint)

            if currentPoint in self.mapPoints:
                currentNode = self.mapPoints[currentPoint]
                if not currentNode.isExplored:
                    hasUnexploredAncestor = True
                    distances.append(dist)

                for dir in currentPoint.availableDirections:
                    nextPoint = Point(currentPoint.x + dir.dx, currentPoint.y + dir.dy)
                    if nextPoint in visitedPoints:
                        continue
                    else:
                        availablePoints.put((nextPoint, dist+1))
            else:
                hasUnexploredAncestor = True
                distances.append(dist)

        if hasUnexploredAncestor:
            return (True, min(distances))
        else:
            return (False, -1)

    def parseDirection(self, direction):
        logger.debug("parsing direction: dx = " + str(direction.dx) + " dy = " + str(direction.dy))
        if direction.dx == 0 and direction.dy == 1:
            return RoboDirection.NORTH
        elif direction.dx == 1 and direction.dy == 0:
            return RoboDirection.EAST
        elif direction.dx == 0 and direction.dy == -1:
            return RoboDirection.SOUTH
        else:
            return RoboDirection.WEST
