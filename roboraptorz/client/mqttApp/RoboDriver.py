import logging

from Common import *

logger = logging.getLogger(__name__)

# Supported Robodriver callbacks
# onStatus(status)
# onDirections(directions)
# onColors(directionColor))
class RoboDriver:
  def __init__(self):
    self.onStatus=None
    self.onDirections=None
    self.onColors=None
    self._discoverMode=false
    self._status=RoboStatus.IDLE

  def driveDirection(direction=RoboDirection.NORTH):
    logger.debug("driveDirection: " str(direction))

  def discoverMode(enabled=false):
    self._discoverMode=enabled
    logger.debug("discoverMode: " str(delf._discoverMode))

  def getDiscoverMode():
    return self._discoverMode

  def getStatus():
    return self._status
