import logging

from Common import *
from Map import *

logger = logging.getLogger(__name__)

class MapMatcher:
    def __init__(self):
        self._roboMaps = {}
        self.onMapUpdate = None
        self.server = None

    def getMap(self, mapName):
        return self._roboMaps[mapName]

    def setServer(self, server):
        self.server = server

    def registerRobotDriver(self, mapName, robotDriver):
        self._roboMaps[mapName] = Map(mapName)
        callback = lambda dirs : self.onDirectionsCallback(mapName, dirs)
        robotDriver.onColors = callback

    def onDirectionsCallback(self, mapName, availableColorsDict):
        logger.debug("onDirectionsCallback")
        roboMap = self._roboMaps[mapName]
        mapFunction = lambda tup : self.mapDirectionAndColorToVectorAndColor(tup)
        mappedDirections = map(mapFunction, availableColorsDict.items())
        roboMap.addDirectionsAtCurrentLocation(mappedDirections)
        if self.onMapUpdate:
            self.onMapUpdate(mapName)
        if self.server:
            self.server.send_update(roboMap)

    def mapDirectionAndColorToVectorAndColor(self, dirColTup):
        direction, color = dirColTup
        mappedColor = LineColor.Black
        logger.debug("mapping color: " + color)
        if color == "R":
            mappedColor = LineColor.Red
        elif color == "B":
            mappedColor = LineColor.Black
        else:
            mappedColor = LineColor.Yellow

        logger.debug("mapping direction " + str(direction))
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
        return (RelativeDirection(dx, dy), mappedColor)
