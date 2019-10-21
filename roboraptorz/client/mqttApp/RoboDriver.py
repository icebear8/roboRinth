import logging

from .Common import *

logger = logging.getLogger(__name__)

# Supported Robodriver callbacks
# onStatus(status)
# onDirections(directions)
# onColors(directionColor))
class RoboDriver:
  def __init__(self, topicPrefix='robo-03'):
    self.onStatus=None
    self.onDirections=None
    self.onColors=None
    self._discoverMode=False
    self._status=RoboStatus.IDLE
    self._topicPrefix=topicPrefix

  def driveDirection(self, direction=RoboDirection.NORTH):
    logger.debug("driveDirection: " + str(direction))

  def discoverMode(self, enabled=False):
    self._discoverMode=enabled
    logger.debug("discoverMode: " + str(self._discoverMode))

  def getDiscoverMode(self):
    return self._discoverMode

  def getStatus(self):
    return self._status
