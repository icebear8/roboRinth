from unittest import TestCase

from graphmap import GraphMap, Edge
from position import Position
from direction import Direction


class TestMap(TestCase):
    def test_get_all_edges(self):
        test_map = GraphMap()
        self.__discover_test_map(test_map)

        def has_edge(position1: Position, position2: Position):
            edge = Edge(test_map._get_and_create_node(position1), test_map._get_and_create_node(position2))
            return edge in test_map.get_all_edges()

        # check edges
        assert (len(test_map.get_all_edges()) == 7)
        assert (has_edge(Position(1, 3), Position(1, 2)))

        assert (has_edge(Position(1, 2), Position(1, 3)))
        assert (has_edge(Position(1, 2), Position(2, 2)))
        assert (has_edge(Position(1, 2), Position(1, 1)))

        assert (has_edge(Position(2, 2), Position(2, 1)))
        assert (has_edge(Position(2, 2), Position(1, 2)))

        assert (has_edge(Position(2, 1), Position(2, 2)))
        assert (has_edge(Position(2, 1), Position(1, 1)))

        assert (has_edge(Position(1, 1), Position(0, 1)))
        assert (has_edge(Position(1, 1), Position(2, 1)))
        assert (has_edge(Position(1, 1), Position(1, 0)))
        assert (has_edge(Position(1, 1), Position(1, 2)))

        assert (has_edge(Position(0, 1), Position(1, 1)))

        assert (has_edge(Position(1, 0), Position(1, 1)))

    def test_visited_nodes(self):
        test_map = GraphMap()
        self.__discover_test_map(test_map)

        def is_visited(position: Position):
            return test_map._get_and_create_node(position).visited

        assert (is_visited(Position(0, 0)) is False)
        assert (is_visited(Position(1, 0)) is False)
        assert (is_visited(Position(2, 0)) is False)
        assert (is_visited(Position(3, 0)) is False)

        assert (is_visited(Position(0, 1)) is False)
        assert (is_visited(Position(1, 1)) is True)
        assert (is_visited(Position(2, 1)) is True)
        assert (is_visited(Position(3, 1)) is False)

        assert (is_visited(Position(0, 2)) is False)
        assert (is_visited(Position(1, 2)) is True)
        assert (is_visited(Position(2, 2)) is True)
        assert (is_visited(Position(3, 2)) is False)

        assert (is_visited(Position(0, 3)) is False)
        assert (is_visited(Position(1, 3)) is True)
        assert (is_visited(Position(2, 3)) is False)
        assert (is_visited(Position(3, 3)) is False)

    def test_available_directions(self):
        test_map = GraphMap()
        self.__discover_test_map(test_map)

        def directions(x, y):
            return test_map.get_available_directions(Position(x, y))

        assert (directions(0, 0) == set())
        assert (directions(1, 0) == {Direction.SOUTH})
        assert (directions(2, 0) == set())
        assert (directions(3, 0) == set())

        assert (directions(0, 1) == {Direction.EAST})
        assert (directions(1, 1) == {Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST})
        assert (directions(2, 1) == {Direction.WEST, Direction.SOUTH})
        assert (directions(3, 1) == set())

        assert (directions(0, 2) == set())
        assert (directions(1, 2) == {Direction.NORTH, Direction.SOUTH, Direction.EAST})
        assert (directions(2, 2) == {Direction.WEST, Direction.NORTH})
        assert (directions(3, 2) == set())

        assert (directions(0, 3) == set())
        assert (directions(1, 3) == {Direction.NORTH})
        assert (directions(2, 3) == set())
        assert (directions(3, 3) == set())

    def test_unvisited_directions(self):
        test_map = GraphMap()
        self.__discover_test_map(test_map)

        def directions(x, y):
            return test_map.get_unvisited_directions(Position(x, y))

        assert (directions(0, 0) == set())
        assert (directions(1, 0) == set())
        assert (directions(2, 0) == set())
        assert (directions(3, 0) == set())

        assert (directions(0, 1) == set())
        assert (directions(1, 1) == {Direction.NORTH, Direction.WEST})
        assert (directions(2, 1) == set())
        assert (directions(3, 1) == set())

        assert (directions(0, 2) == set())
        assert (directions(1, 2) == set())
        assert (directions(2, 2) == set())
        assert (directions(3, 2) == set())

        assert (directions(0, 3) == set())
        assert (directions(1, 3) == set())
        assert (directions(2, 3) == set())
        assert (directions(3, 3) == set())

    @staticmethod
    def __discover_test_map(map: GraphMap):
        # discover test map
        #
        #   0   1   2   3
        #   *   *   *   *  0
        #       |
        #   * - * - *   *  1
        #       |   |
        #   *   * - *   *  2
        #       |
        #   *   *   *   *  3

        map.node_discovered(Position(1, 3), {Direction.NORTH})
        map.node_discovered(Position(1, 2), {Direction.NORTH, Direction.EAST})
        map.node_discovered(Position(2, 2), {Direction.NORTH, Direction.WEST})
        map.node_discovered(Position(2, 1), {Direction.SOUTH, Direction.WEST})
        map.node_discovered(Position(1, 1), {Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST})
