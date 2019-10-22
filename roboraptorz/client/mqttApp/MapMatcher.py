import logging

from Common import *
from Map import *

logger = logging.getLogger(__name__)

class MapMatcher:
    def __init__(self):
        self._roboMaps = {}
        self.onMapUpdate = None

    def getMap(self, mapName):
        return self.roboMaps[mapName]

    def registerRobotDriver(self, mapName, robotDriver):
        self._roboMaps[mapName] = Map(mapName)
        callback = lambda dirs : self.onDirectionsCallback(mapName, dirs)
        robotDriver.onDirections = callback

    def onDirectionsCallback(self, mapName, availableDirections):
        map = self._roboMaps[mapName]
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
