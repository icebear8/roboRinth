
import logging

logger = logging.getLogger(__name__)

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

class RelativeDirection:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

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

    def __init__(self, mapName):
        self._mapName = mapName
        self.mapPoints = []
        self.pointsOfInteres = {}
        self.setRobotLocation(Point(0, 0))

    def addMapPoint(self,  direction):
        p, d = direction
        logger.debug(self._mapName + ": setting connection from (" + str(p.x) + "," + str(p.y) + ") to (" + str(d.dx) + "," + str(d.dy) + ")")
        self.mapPoints.append(direction)

    def setRobotLocation(self, point):
        logger.debug(self._mapName + ": setting robot location at (" + str(point.x) + "," + str(point.y) + ")")
        self.pointsOfInteres[self.ROBOT_LOCATION_KEY] = point

    def getRobotLocation(self):
        return self.pointsOfInteres[self.ROBOT_LOCATION_KEY]

    def setStartPoint(self, point):
        logger.debug(self._mapName + ": setting start location at (" + str(point.x) + "," + str(point.y) + ")")
        self.pointsOfInteres[self.START_POINT_KEY] = point

    def setSyncLine(self, direction):
        p,d = direction
        logger.debug(self._mapName + ": setting sync line from (" + str(p.x) + "," + str(p.y) + ") to (" + str(d.dx) + "," + str(d.dy) + ")")
        self.pointsOfInteres[self.SYNC_LINE_KEY] = direction

    def getAvailableDirections(self):
        return [ AvailableDirection() ]