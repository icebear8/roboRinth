
import logging
import random
import sys
from map import Map
from map import Position
from map import Direction
from Path import PathDiscovery

logger = logging.getLogger(__name__)



class Control:
  def __init__(self, theMap, mqttCom, pathFinder):
    self._map = theMap
    self._mqttCom = mqttCom
    self._path = pathFinder

  def onHandleCrossingReached(self):
    self._path.handle_crossing_reached()
    logger.debug("onHandleCrossingReached")

  def onHandleDiscoveryFinished(self, direction: Direction):
    logger.debug("onHandleDiscoveryFinished:" + str(direction))
    self._map.node_discovered(self._path.get_current_position(), direction)

