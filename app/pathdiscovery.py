from enum import Enum, IntEnum
from typing import Set
from graphmap import Node
from position import Position
from direction import Direction


class Action(IntEnum):
    GO_NORTH = 0,
    GO_EAST = 1,
    GO_SOUTH = 2,
    GO_WEST = 3,
    DO_DISCOVERY = 4,
    DO_ABORT = 5,


class PathDiscovery:
    def __init__(self, refmap):
        self.__map = refmap
        self.__currentNode = refmap.get_node(Position(0, 0))
        self.__currentDirection = Direction.NORTH
        self.__pathList = []

    def get_current_position(self) -> Position:
        return self.__currentNode.position

    def handle_crossing_reached(self) -> Action:
        if self.__currentNode.visited:
            action = self.__forward_step()
            return action
        else:
            print("PATH: doDiscovery")
            return Action.DO_DISCOVERY

    def handle_discovery_finished(self) -> Action:
        action = self.__forward_step()
        return action

    def __forward_step(self) -> Action:
        print("PATH: forward")
        new_directions = self.__map.get_unvisited_directions(self.__currentNode.position)
        print(new_directions)
        action = self.__convert_direction_to_action(self.__get_most_left_direction(new_directions))
        if action is None:
            action = self.__return_step()
        else:
            self.__set_new_position(self.convert_action_to_direction(action))
        print("PATH: action " + str(action))
        return action

    def __return_step(self) -> Action:
        print("PATH: return")
        try:
            return_point =  self.__pathList.pop()
        except:
            return Action.DO_ABORT
        returnDirection = self.__calculate_direction(self.__currentNode, return_point)
        self.__currentNode = return_point
        self.__currentDirection = returnDirection
        action = self.__convert_direction_to_action(returnDirection)
        return action

    def __set_new_position(self, direction: Direction):
        self.__pathList.append(self.__currentNode)
        newPos = self.__currentNode.position.new_pos_in_direction(direction, 1)
        self.__currentNode = self.__map.get_node(newPos)
        self.__currentDirection = direction

    def __calculate_direction(self, a: Node, b: Node) -> Direction:
        if a.position.x > b.position.x:
            return Direction.WEST
        elif a.position.x < b.position.x:
            return Direction.EAST
        elif a.position.y > b.position.y:
            return Direction.NORTH
        else:
            return Direction.SOUTH

    def __convert_direction_to_action(self, dir: Direction) -> Action:
        lookup = {Direction.NORTH: Action.GO_NORTH,
                  Direction.EAST: Action.GO_EAST,
                  Direction.SOUTH: Action.GO_SOUTH,
                  Direction.WEST: Action.GO_WEST,
                  None: None,
                  }
        return lookup[dir]

    def convert_action_to_direction(self, action: Action) -> Direction:
        lookup = {
            Action.GO_NORTH: Direction.NORTH,
            Action.GO_EAST: Direction.EAST,
            Action.GO_SOUTH: Direction.SOUTH,
            Action.GO_WEST: Direction.WEST,
        }
        return lookup[action]

    def __get_most_left_direction(self, directions: Set[Direction]) -> Direction:
        if Direction((int(self.__currentDirection) + int(Direction.WEST)) % 4) in directions:
            ret = Direction((int(self.__currentDirection) + int(Direction.WEST)) % 4)
        elif self.__currentDirection in directions:
            ret = self.__currentDirection
        elif Direction(int(self.__currentDirection + int(Direction.EAST)) % 4) in directions:
            ret = Direction(int(self.__currentDirection + int(Direction.EAST)) % 4)
        else:
            ret = None
        return ret


class PathSimple:
    def __init__(self):
        pass

    def handle_crossing_reached(self):
        pass

    def handle_discovery_finished(self):
        pass


class PathFastReturn:
    def __init__(self):
        pass

    def handle_crossing_reached(self):
        pass

    def handle_discovery_finished(self):
        pass
