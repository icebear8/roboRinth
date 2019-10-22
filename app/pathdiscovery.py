from enum import Enum, IntEnum
from typing import Set
from graphmap import Node
from position import Position
from direction import Direction


class Action(IntEnum):
    goNorth = 0,
    goEast = 1,
    goSouth = 2,
    goWest = 3,
    doDiscovery = 4,
    doAbort = 5,


class PathDiscovery:
    def __init__(self, refmap):
        self.__map = refmap
        self.__current_position = Position(0, 0)
        self.__currentDirection = Direction.NORTH
        self.__pathList = []

    def get_current_position(self) -> Position:
        return self.__current_position

    def handle_crossing_reached(self) -> Action:
        if self.__map.get_node(self.__current_position).visited:
            action = self.__forward_step()
            print("number of unvisited" + str(self.__map.get_number_of_unvisited_nodes()))

            return action
        else:
            print("PATH: doDiscovery")
            return Action.doDiscovery

    def handle_discovery_finished(self) -> Action:
        action = self.__forward_step()
        return action

    def __forward_step(self) -> Action:
        print("PATH: forward")
        new_directions = self.__map.get_unvisited_directions(self.__current_position)
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
            return_point = self.__pathList.pop()
        except:
            return Action.doAbort
        returnDirection = self.__calculate_direction(self.__current_position, return_point.position)
        self.__current_position = return_point.position
        self.__currentDirection = returnDirection
        action = self.__convert_direction_to_action(returnDirection)
        return action

    def __set_new_position(self, direction: Direction):
        self.__pathList.append(self.__map.get_node(self.__current_position))
        self.__current_position =  self.__current_position.new_pos_in_direction(direction, 1)
        self.__currentDirection = direction

    def __calculate_direction(self, a: Position, b: Position) -> Direction:
        if a.x > b.x:
            return Direction.WEST
        elif a.x < b.x:
            return Direction.EAST
        elif a.y > b.y:
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

    def convert_action_to_direction(self, action: Action) -> Direction:
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
