
import logging
import random
import sys
from map import Map
from map import Position
from map import Direction

logger = logging.getLogger(__name__)



class Control:
  def __init__(self, theMap, mqttCom):
    self._map = theMap
    self._mqttCom = mqttCom

  def onHandleCrossingReached(self):
    logger.debug("onHandleCrossingReached")

  def onHandleDiscoveryFinished(self, direction: Direction):
    logger.debug("onHandleDiscoveryFinished:" + str(direction))
    currentPosition = Position(0,2)
    directions = {Direction.NORTH, Direction.EAST}
    self._map.node_discovered(currentPosition, directions)


   
