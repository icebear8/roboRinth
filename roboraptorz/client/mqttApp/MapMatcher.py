import logging

from Common import *
from Map import *

logger = logging.getLogger(__name__)

class MapMatcher:
    def __init__(self):
        self.globalMap = Map()
        self.roboMaps = {}

    def registerRobotDriver(self, robotId, robotDriver):
        self.roboMaps[robotId] = Map()
        callback = lambda dirs : self.onDirectionsCallback(robotId, dirs)
        robotDriver.onDirections = callback

    def onDirectionsCallback(self, robotId, availableDirections):
        map = self.roboMaps[robotId]
        currentPosition = map.getRobotLocation()
        for direction in availableDirections:
            dx = 0
            dy = 0
            if direction == RoboDirection.NORTH:
                dx = 0
                dy = 1
            elif direction == RoboDirection.EAST:
                dx = 1
                dy = 0
            elif direction == RoboDirection.SOUTH:
                dx = 0
                dy = -1
            else:
                dx = -1
                dy = 0
            relativeDirection = RelativeDirection(dx, dy)
            map.addMapPoint((currentPosition, relativeDirection))
