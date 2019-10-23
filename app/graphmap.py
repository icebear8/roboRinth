from typing import Set, List, Tuple, Union

from direction import Direction
from position import Position
from color import Color


class Node:
    def __init__(self, position: Position):
        self.position = position
        self.visited = False


class Edge:
    def __init__(self, node1: Node, node2: Node, color: Color):
        self.node1 = node1
        self.node2 = node2
        self.color = color


class GraphMap:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def node_discovered(self, position: Position, available_directions: List[Tuple[Direction, Color]]):
        node = self.__get_or_create_node(position)
        node.visited = True

        for direction in available_directions:
            self.__get_or_create_edge(position, direction[0], direction[1])

    def get_available_directions(self, position: Position) -> Set[Direction]:
        result = set()
        for direction in Direction:
            edge = self.get_edge(position, direction)
            if edge:
                result.add(direction)
        return result

    def get_unvisited_directions(self, position: Position) -> Set[Direction]:
        result = set()
        for direction in Direction:
            node = self.get_node(position.new_pos_in_direction(direction))
            if node and node.visited:
                continue
            edge = self.get_edge(position, direction)
            if edge:
                result.add(direction)
        return result

    def get_node(self, position: Position) -> Union[Node, None]:
        for node in self.nodes:
            if node.position == position:
                return node

        return None

    def get_edge(self, position: Position, direction: Direction) -> Union[Edge, None]:
        pos1 = position
        pos2 = position.new_pos_in_direction(direction)

        for edge in self.edges:
            if edge.node1.position == pos1 and edge.node2.position == pos2 or \
                    edge.node1.position == pos2 and edge.node2.position == pos1:
                return edge

        return None

    def get_all_edges(self) -> List[Edge]:
        return self.edges

    def get_number_of_unvisited_nodes(self):
        return sum([not node.visited for node in self.nodes])

    def __get_or_create_node(self, position: Position) -> Node:
        node = self.get_node(position)
        if not node:
            node = Node(position)
            self.nodes.append(node)
        return node

    def __get_or_create_edge(self, position: Position, direction: Direction, color: Color) -> Edge:
        edge = self.get_edge(position, direction)

        if not edge:
            node1 = self.__get_or_create_node(position)
            node2 = self.__get_or_create_node(position.new_pos_in_direction(direction))
            edge = Edge(node1, node2, color)
            self.edges.append(edge)

        return edge

