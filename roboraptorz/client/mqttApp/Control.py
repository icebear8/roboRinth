
import logging
import threading

from Map import *
from MapMatcher import *
from RoboDriver import *

logger = logging.getLogger(__name__)

class Control:
  def __init__(self, roboName, mapMatcher, roboDriver):
    self.roboName=roboName

    self._roboDriver=roboDriver
    self._roboDriver.onStatus=self._onRoboStatus

    self._mapMatcher=mapMatcher
    self._mapMatcher.onMapUpdate=self._onMapUpdate

  def start(self):
    self._map.setRobotLocation(Point(0,0))
    self._roboDriver.discoverMode(True)

  def _map(self):
    return self._mapMatcher.getMap(self.roboName)

  # Callbacks map
  def _onMapUpdate(mapName):
    if mapName in (self.roboName):
      logger.debug(self.roboName + "OnMapUpdate: " + mapName)
      self._triggerExploreStep()

  # Callbacks driver
  def _onRoboStatus(self, status):
    logger.debug(self.roboName + "OnRoboStatus: " + str(status))
    if status is RoboStatus.IDLE:
      self._triggerExploreStep()


  def _triggerExploreStep(self):
    timer = threading.Timer(1, self._executeExploreStep())
    timer.start()

  def _executeExploreStep(self):
    if self._roboDriver.getStatus() is RoboStatus.IDLE:
      nextDirection = _calcNextExploreStep()
      logger.debug(self.roboName + "exploreStep, nextStep to be executed: " + str(nextDirection))
      if nextDirection:
        self._move(nextDirection)

  def _calcNextExploreStep():
    directions = self._map().getAvailableDirections()
    logger.debug(self.roboName + "calcNextExploreStep, available directions: " + str(directions))

    # find unexplored neighbours
    unexplored = filter(lambda element: element.explored==False, directions)
    if unexplored:
      logger.debug(self.roboName + "calcNextExploreStep, unexplored list: " + str(unexplored))
      sortedDir = unexplored.sort(key=lambda element: element.direction)
      return sortedDir[0].direction

    # find closest unexplored child
    unexploredChild = filter(lambda element: element.hasUnexploredChildren==True, directions)
    if unexploredChild:
      logger.debug(self.roboName + "calcNextExploreStep, unexploredChildren list: " + str(unexploredChild))
      sortedDir = unexploredChild.sort(key=lambda element: element.distanceToUnexplored)
      return sortedDir[0].direction

    logger.info(self.roboName + "calcNextExploreStep, No unexplored neighbours or children!")
    return None

  def _move(direction=RoboDirection.NORTH):
    nextPosition=self._map().getRobotLocation().move(direction)
    self._map().setRobotLocation(nextPosition)
    self._roboDriver.driveDirection(direction)
