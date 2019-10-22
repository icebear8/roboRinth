
import logging

from Map import *
from MapMatcher import *
from RoboDriver import *

logger = logging.getLogger(__name__)

class Control:
  def __init__(self, roboName='roboraptorz', mapMatcher, roboDriver):
    self.roboName=roboName

    self._roboDriver=roboDriver
    self._roboDriver.onStatus=self._onRoboStatus
    self._roboDriver.onColors=self._onRoboColors

    self._mapMatcher=mapMatcher
    self._mapMatcher.onMapUpdate=self._onMapUpdate

  def start(self):
    self._map.setRobotLocation(Point(0, 0))
    self._roboDriver.discoverMode(True)

  def _map(self):
    return self._mapMatcher.getMap(self.roboName)

  # Callbacks map
  def _onMapUpdate(mapName):
    if mapName in (self.roboName):
      logger.debug(self.roboName + "OnMapUpdate: " + mapName)

  # Callbacks driver
  def _onRoboStatus(self, status):
    logger.debug(self.roboName + "OnRoboStatus: " + str(status))

  def _onRoboColors(self, colors):
    logger.debug(self.roboName + "OnRoboColors: " + str(colors))

  def _exploreStep(self):
    if self._roboDriver.getStatus() is RoboStatus.IDLE:
      nextStep =
      self._roboDriver.driveDirection()

  def _calcNextExploreStep():
    pass
