
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

    def __str__(self):
        return "(x: " + str(self.x) + ", y: " + str(self.y) + ")"

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

    def __str__(self):
        return "(dx: " + str(self.dx) + ", dy: " + str(self.dy) + ")"

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
        self.LineColor = LineColor.Black

    def hasUnexploredChildren(self):
        if self.distanceToUnexplored == -1:
            return False
        return True

    def __str__(self):
        return "AvDir(dir: " + DirToStr(self.direction) + ", lineColor: " + LineColorToStr(self.LineColor) + ", explored: " + str(self.explored) + ", distance: " + str(self.distanceToUnexplored) + ", hasUnexpChildren: " + str(self.hasUnexploredChildren()) + ")"

class Map:
    ROBOT_LOCATION_KEY = "robotLocation"
    START_POINT_KEY = "startPoint"
    SYNC_LINE_KEY = "syncLine"

    class MapNode:
        def __init__(self, coords):
            self.coord = coords
            self.isExplored = False
            self.availableDirections = []

        def addAvailableDirection(self, directionWithColor):
            if not(directionWithColor in self.availableDirections):
                self.availableDirections.append(directionWithColor)

    def __init__(self, mapName):
        initalLocation = Point(0,0)
        self._mapName = mapName
        self._roboLocation = initalLocation
        self.mapPoints = { initalLocation: self.MapNode(initalLocation)}
        self.pointsOfInterest = {}

    def addDirectionsAtCurrentLocation(self, directionsWithColors):
        point = self.getRobotLocation()
        mapPoint = self.mapPoints[point]
        for directionWithColor in directionsWithColors:
            direction, color = directionWithColor
            logger.debug(self._mapName + ": setting connection from (" + str(point.x) + "," + str(point.y) + ") to (" + str(direction.dx) + "," + str(direction.dy) + ") with color " + LineColorToStr(color))
            mapPoint.addAvailableDirection(directionWithColor)

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
        logger.debug("getAvailableDirections at location " + str(loc))
        result = []
        for dir, color in availableDirections:
            logger.debug("available direction " + DirToStr(self.parseDirection(dir)) + " with color " + LineColorToStr(color))
            newPoint = Point(loc.x + dir.dx, loc.y + dir.dy)
            logger.debug("next possible point: " + str(newPoint))
            if newPoint in self.mapPoints:
                logger.debug("next possible point was visited")
                nextNode = self.mapPoints[newPoint]
                hasUnexploredChildren, distance = self._hasNodeUnexploredChildren(nextNode)
                availableDirection = AvailableDirection()
                availableDirection.direction = self.parseDirection(dir)
                availableDirection.explored = nextNode.isExplored
                availableDirection.distanceToUnexplored = distance
                availableDirection.LineColor = color
                result.append(availableDirection)
            else:
                logger.debug("next possible point was not visited")
                availableDirection = AvailableDirection()
                availableDirection.direction = self.parseDirection(dir)
                availableDirection.explored = False
                availableDirection.distanceToUnexplored = 0
                availableDirection.LineColor = color
                result.append(availableDirection)
        logger.debug("found " + str(len(result)) + " available directions")
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

                for dir, color in currentNode.availableDirections:
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
