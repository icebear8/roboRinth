from enum import Enum
from typing import Set
from app.map import Direction, Position, Node


class Action(Enum):
    goNorth = 0,
    goEast = 1,
    goSouth = 2,
    goWest = 3,
    doDiscovery = 4,


class PathDiscovery:
    def __init__(self, refmap):
        self.__map = refmap
        self.__currentNode = refmap.get_node(Position(0, 0))
        self.__currentDirection = Direction.NORTH
        self.__pathList = []
        self.__currentNode = None

    def handle_crossing_reached(self) -> Action:
        if self.__currentNode.visited:
            return_direction = self.__calculate_direction(self.__currentNode, self.__pathList.pop())
            action = self.__convert_direction_to_action(return_direction)
            self.__set_new_position(self.__convert_action_to_direction(action))
            return action
        else:
            return Action.doDiscovery

    def handle_discovery_finished(self) -> Action:
        new_directions = self.__map.get_unvisited_directions(self.__currentNode.position)
        action = self.__convert_direction_to_action(self.__get_most_left_direction(new_directions))
        if action is None:
            returnDirection = self.__calculate_direction(self.__currentNode, self.__pathList.pop())
            action = self.__convert_direction_to_action(returnDirection)

        self.__set_new_position(self.__convert_action_to_direction(action))
        return action

    def __set_new_position(self, direction: Direction):
        self.__pathList.append(self.__currentNode)
        newPos = self.__currentNode.position.new_pos_in_direction(direction, 1)
        self.__currentNode = self.__map.get_node(newPos)
        self._currentDirection = direction

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
        lookup = {Direction.NORTH: Action.goNorth,
                  Direction.EAST: Action.goEast,
                  Direction.SOUTH: Action.goSouth,
                  Direction.WEST: Action.goWest,
                  None: None,
                  }
        return lookup[dir]

    def __convert_action_to_direction(self, action: Action) -> Direction:
        lookup = {
            Action.goNorth: Direction.NORTH,
            Action.goEast: Direction.EAST,
            Action.goSouth: Direction.SOUTH,
            Action.goWest: Direction.WEST,
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
