from unittest import TestCase

from map import Map, Position, Direction, Edge


class TestMap(TestCase):
    def test_get_all_edges(self):
        map = Map()
        self.__discover_test_map(map)

        # check edges
        assert(len(map.get_all_edges()) == 7)
        assert(self.__map_has_edge(map, Position(1, 3), Position(1, 2)))

        assert(self.__map_has_edge(map, Position(1, 2), Position(1, 3)))
        assert(self.__map_has_edge(map, Position(1, 2), Position(2, 2)))
        assert(self.__map_has_edge(map, Position(1, 2), Position(1, 1)))

        assert(self.__map_has_edge(map, Position(2, 2), Position(2, 1)))
        assert(self.__map_has_edge(map, Position(2, 2), Position(1, 2)))

        assert(self.__map_has_edge(map, Position(2, 1), Position(2, 2)))
        assert(self.__map_has_edge(map, Position(2, 1), Position(1, 1)))

        assert(self.__map_has_edge(map, Position(1, 1), Position(0, 1)))
        assert(self.__map_has_edge(map, Position(1, 1), Position(2, 1)))
        assert(self.__map_has_edge(map, Position(1, 1), Position(1, 0)))
        assert(self.__map_has_edge(map, Position(1, 1), Position(1, 2)))

        assert(self.__map_has_edge(map, Position(0, 1), Position(1, 1)))

        assert(self.__map_has_edge(map, Position(1, 0), Position(1, 1)))

    @staticmethod
    def __discover_test_map(map: Map):
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

    @staticmethod
    def __map_has_edge(map: Map, position1: Position, position2: Position):
        edge = Edge(map.get_node(position1), map.get_node(position2))
        return edge in map.get_all_edges()

