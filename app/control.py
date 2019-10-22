import logging
import random
import sys
from app.map import Map
from app.map import Position
from app.map import Direction
from app.Path import PathDiscovery, Action
from typing import List, Tuple

logger = logging.getLogger(__name__)


class Control:
    def __init__(self, theMap, mqttCom, pathFinder):
        self._map = theMap
        self._mqttCom = mqttCom
        self._path = pathFinder

    def onHandleCrossingReached(self):
        print("onHandleCrossingReached")
        action = self._path.handle_crossing_reached()
        self.handle_action(action)

    def handle_action(self, action: Action):
        if action == Action.doDiscovery:
            self._mqttCom.discover_directions()
        elif action is None:
            pass
        elif action == Action.doAbort:
            print("I have seen the whole world. Roger an out!")
            sys.exit(0)
        else:
            self._mqttCom.drive_direction(self._path.convert_action_to_direction(action))

    def onHandleDiscoveryFinished(self, direction: List[ Tuple(Direction, Color)])
        action = self._path.handle_discovery_finished()
        self.handle_action(action)
