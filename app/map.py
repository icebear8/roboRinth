from enum import Enum
from typing import Set, List


class Direction(Enum):
    NORTH = 0,
    EAST = 1,
    SOUTH = 2,
    WEST = 3,


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Node:
    def __init__(self, position: Position, visited: bool):
        self.position = position
        self.visited = visited


class Edge:
    def __init__(self, node1: Node, node2: Node):
        self.node1 = node1
        self.node2 = node2


class Map:
    def __init__(self):
        pass

    def node_discovered(self, position: Position, available_directions: Set[Direction]):
        pass

    def get_node(self, position: Position) -> Node:
        pass

    def get_available_directions(self, position: Position) -> Set[Direction]:
        pass

    def get_new_directions(self, position: Position) -> Set[Direction]:
        pass

    def get_all_edges(self) -> List[Edge]:
        pass
