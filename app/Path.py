from enum import Enum
from typing import Set, List
from app.map import Direction, Position, Position, Node


class Action(Enum):
    goNorth = 0,
    goEast = 1,
    goSouth = 2,
    goWest = 3,
    doDiscovery = 4,


class PathDiscovery:
    def __init__(self, map):
        self.__map = map
        self.__currentNode = map.get_node( Position(0,0) )
        self.__currentDirection = Direction.NORTH

    def handleCrossingReached(self) -> Action:
        newDirections = self.__map.get_unvisited_directions(self.__currentNode.position)
        action = self.__convertDirectionToAction(self.__getMostLeftDirection(newDirections))
        if(action == None):
            returnDirection = self.__calculateDirection(self.__currentNode, self.pathList.pop())
            action = self.__convertDirectionToAction(returnDirection)
        else:
            self.__setNewPosition(self.__convertActionToDirection(action))
        return action

    def __setNewPosition(self, direction : Direction) :
        self.pathList.append(self.__currentNode)
        newPos = self.__currentNode.position.new_pos_in_direction(direction, 1);
        self.__currentNode = self.__map.get_node(newPos)
        self._currentDirection = direction

    def __calculateDirection(self, A : Node, B : Node) -> Direction:
        if(A.position.x > B.position.x):
            return Direction.WEST
        elif(A.position.x < B.position.x):
            return Direction.EAST
        elif(A.position.y > B.position.y):
            return Direction.NORTH
        else:
            return Direction.SOUTH

    def __convertDirectionToAction(self, dir : Direction) -> Action:
        lookup = {Direction.NORTH : Action.goNorth,
                  Direction.EAST: Action.goEast,
                  Direction.SOUTH: Action.goSouth,
                  Direction.WEST: Action.goWest,
                  None : None,
                  }
        return lookup[dir]

    def __convertActionToDirection(self, action : Action) -> Direction:
        lookup = { Action.goNorth : Direction.NORTH,
                  Action.goEast : Direction.EAST,
                  Action.goSouth : Direction.SOUTH,
                  Action.goWest : Direction.WEST,
                  }
        return lookup[action]

    def __getMostLeftDirection(self, directions : Set[Direction]) -> Direction:
        ret = None
        if Direction( (int(self.__currentDirection) + int(Direction.WEST)) % 4) in directions:
            ret = self.Direction( (int(self.__currentDirection) + int(Direction.WEST)) % 4)
        elif self.__currentDirection in directions:
            ret =  self.__currentDirection
        elif Direction(int( (self.__currentDirection) + int(Direction.EAST)) % 4) in directions:
            ret =  Direction(int( (self.__currentDirection) + int(Direction.EAST)) % 4)
        else:
            ret = None;
        return ret

    def handleDiscoveryFinished(self) -> Action:
        action = Action.goNorth
        if(action == Action.goNorth):
            pass
        elif(action == Action.goSouth):
            pass
        elif(action == Action.goWest):
            pass
        else:
            pass
        return action;

    pathList = []
    _currentNode = None
    _currentDirection = None

class PathSimple:
    def __init__(self):
        pass
    def handleCrossingReached(self):
        pass

    def handleDiscoveryFinished(self):
        pass

class PathFastReturn:
    def __init__(self):
        pass
    def handleCrossingReached(self):
        pass

    def handleDiscoveryFinished(self):
        pass