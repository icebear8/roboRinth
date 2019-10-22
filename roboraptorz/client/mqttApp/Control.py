
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

    self._timerPending = False

  def start(self):
    startPoint = Point(0,0)
    self._map().setStartPoint(startPoint)
    self._map().setRobotLocation(startPoint)
    #self._roboDriver.discoverMode(True)

  def _map(self):
    return self._mapMatcher.getMap(self.roboName)

  # Callbacks map
  def _onMapUpdate(self, mapName):
    if mapName not in (self.roboName):
      return

    logger.debug(self.roboName + "OnMapUpdate: " + mapName)
    if (self._roboDriver.getStatus() is RoboStatus.IDLE) and (self._roboDriver.getDiscoverMode() is True):
      self._triggerExploreStep()

  # Callbacks driver
  def _onRoboStatus(self, status):
    logger.debug(self.roboName + "OnRoboStatus: " + str(status))
    if (status is RoboStatus.IDLE) and (self._roboDriver.getDiscoverMode() is True):
      self._triggerExploreStep()


  def _triggerExploreStep(self):
    if not self._timerPending:
      self._timerPending = True
      timer = threading.Timer(1.0, self._executeExploreStep)
      timer.start()

  def _executeExploreStep(self):
    self._timerPending = False
    if self._roboDriver.getStatus() is RoboStatus.IDLE:
      nextDirection = self._calcNextExploreStep()
      logger.debug(self.roboName + "exploreStep, nextStep to be executed: " + str(nextDirection))
      if nextDirection:
        self._move(nextDirection)

  def _calcNextExploreStep(self):
    directions = self._map().getAvailableDirections()
    logger.debug(self.roboName + " calcNextExploreStep, available directions count: " + str(len(directions)) + " :")
    for dir in directions:
        logger.debug("\t" + str(dir))
    # find unexplored neighbours
    unexplored = list(filter(lambda element: element.explored==False, directions))
    if len(unexplored):
      logger.debug(self.roboName + " calcNextExploreStep, unexplored list count: " + str(len(unexplored)) + " :")
      for dir in unexplored:
          logger.debug("\t" + str(dir))
      unexplored.sort(key=lambda element: DirectionSortOrder(element.direction))
      return unexplored[0].direction

    # find closest unexplored child
    unexploredChild = list(filter(lambda element: element.hasUnexploredChildren()==True, directions))
    if unexploredChild:
      logger.debug(self.roboName + " calcNextExploreStep, unexploredChildren list count: " + str(len(unexploredChild)) + " :")
      for dir in unexploredChild:
          logger.debug("\t" + str(dir))
      unexploredChild.sort(key=lambda element: element.distanceToUnexplored)
      return unexploredChild[0].direction

    logger.info(self.roboName + "calcNextExploreStep, No unexplored neighbours or children!")
    return None

  def _move(self, direction=RoboDirection.NORTH):
    nextPosition=self._map().getRobotLocation().move(direction)
    self._map().setRobotLocation(nextPosition)
    self._roboDriver.driveDirection(direction)
