from enum import Enum
from typing import Set


class Direction(Enum):
    NORTH = 0,
    EAST = 1,
    SOUTH = 2,
    WEST = 3,


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def new_pos_in_direction(self, direction: Direction, distance: 1) -> 'Position':
        offsets = {
            Direction.NORTH: Position(0, -distance),
            Direction.EAST: Position(distance, 0),
            Direction.SOUTH: Position(0, distance),
            Direction.WEST: Position(-distance, 0),
        }
        return self + offsets[direction]


    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)


class Node:
    def __init__(self, position: Position):
        self.position = position
        self.visited = False


class Edge:
    def __init__(self, node1: Node, node2: Node):
        self.node1 = node1
        self.node2 = node2

    def __hash__(self):
        return hash({self.node1, self.node2})

    def __eq__(self, other):
        return {self.node1, self.node2} == {other.node1, other.node2}


class Map:
    def __init__(self):
        self.nodes = dict()
        self.edges = set()

    def node_discovered(self, position: Position, available_directions: Set[Direction]):
        node = self.get_node(position)
        node.visited = True

        for direction in available_directions:
            self.edges.add(self.__create_edge(position, direction))

    def get_available_directions(self, position: Position) -> Set[Direction]:
        result = set()
        for direction in Direction:
            if self.__create_edge(position, direction) in self.edges:
                result.add(direction)
        return result

    def get_unvisited_directions(self, position: Position) -> Set[Direction]:
        result = set()
        for direction in Direction:
            if self.get_node(position.new_pos_in_direction(direction, 1)).visited:
                continue
            if self.__create_edge(position, direction) in self.edges:
                result.add(direction)
        return result

    def get_node(self, position: Position) -> Node:
        if position not in self.nodes:
            self.nodes[position] = Node(position)
        return self.nodes[position]

    def get_all_edges(self) -> Set[Edge]:
        return self.edges

    def __create_edge(self, position: Position, direction: Direction):
        node1 = self.get_node(position)
        node2 = self.get_node(position.new_pos_in_direction(direction, 1))
        return Edge(node1, node2)
