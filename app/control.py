
import logging
import random
import sys
from graphmap import GraphMap
from position import Position
from direction import Direction
from pathdiscovery import PathDiscovery, Action

logger = logging.getLogger(__name__)



class Control:
  def __init__(self, theMap, mqttCom, pathFinder, server):
    self._map = theMap
    self._mqttCom = mqttCom
    self._path = pathFinder
    self._server = server

  def onHandleCrossingReached(self):
    print("onHandleCrossingReached")
    self._server.send_update(self._map, self._path.get_current_position())
    action = self._path.handle_crossing_reached()
    self.handle_action(action)

  def handle_action(self, action : Action):
    if action == Action.doDiscovery:
      self._mqttCom.discover_directions()
    elif action == None:
      pass
    elif action == Action.doAbort:
      print("I have seen the whole world. Roger an out!")
      sys.exit(0)
    else:
      self._mqttCom.drive_direction(self._path.convert_action_to_direction(action))

  def onHandleDiscoveryFinished(self, direction: Direction):
    print("onHandleDiscoveryFinished:" + str(direction))
    self._map.node_discovered(self._path.get_current_position(), direction)
    self._server.send_update(self._map, self._path.get_current_position())
    action = self._path.handle_discovery_finished()
    self.handle_action(action)