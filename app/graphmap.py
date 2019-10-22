from typing import Set, List, Tuple

from direction import Direction
from position import Position
from color import Color

class Node:
    def __init__(self, position: Position):
        self.position = position
        self.visited = False

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.position)


class Edge:
    def __init__(self, node1: Node, node2: Node, color: Color):
        self.node1 = node1
        self.node2 = node2
        self.color = color

    def __hash__(self):
        #color ignored by purpose
        return hash(self.node1) | hash(self.node2)

    def __eq__(self, other):
        #color ignored purpose
        return {self.node1, self.node2} == {other.node1, other.node2}


class GraphMap:
    def __init__(self):
        self.nodes = dict()
        self.edges = set()

    def node_discovered(self, position: Position, available_directions: List[Tuple[Direction, Color]]):
        node = self._get_and_create_node(position)
        node.visited = True

        for direction in available_directions:
            self.edges.add(self.__create_edge(position, direction))
            if direction[0] == Color.RED:
                print('We found the treasure!!')

    def get_edge_color(self, position, direction):
        for e in self.edges:
            if (e == self.__create_edge(position, direction)):
                return e.color
        return None

    def get_available_directions(self, position: Position) -> Set[Direction]:
        result = set()
        for direction in Direction:
            if self.__create_edge(position, (direction, Color.BLACK)) in self.edges:
                result.add(direction)
        return result

    def get_unvisited_directions(self, position: Position) -> Set[Direction]:
        result = set()
        for direction in Direction:
            if self._get_and_create_node(position.new_pos_in_direction(direction, 1)).visited:
                continue
            if self.__create_edge(position, (direction, Color.BLACK)) in self.edges:
                result.add(direction)
        return result

    def _get_and_create_node(self, position: Position) -> Node:
        if position not in self.nodes:
            self.nodes[position] = Node(position)
        return self.nodes[position]

    def get_node(self, position: Position) -> Node:
        if position not in self.nodes:
            return None
        return self.nodes[position]

    def get_all_edges(self) -> Set[Edge]:
        return self.edges

    def get_number_of_unvisited_nodes(self):
        return sum([not node.visited for node in self.nodes.values()])


    def __create_edge(self, position: Position, direction: Tuple[Direction, Color]):
        node1 = self._get_and_create_node(position)
        node2 = self._get_and_create_node(position.new_pos_in_direction(direction[0], 1))
        return Edge(node1, node2, direction[1])
