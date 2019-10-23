from unittest import TestCase
from unittest.mock import MagicMock

from direction import Direction
from graphmap import GraphMap, Node
from pathdiscovery import PathDiscovery, Action
from position import Position


class TestPathDiscovery(TestCase):
    def test_handleCrossingReached(self):
        pass

    def test_handleDiscoveryFinished(self):
        map = GraphMap()
        pos = Position(0, 0)
        map.__get_or_create_node = MagicMock(return_value=Node(pos))
        path = PathDiscovery(map)

        # go west
        map.get_unvisited_directions = MagicMock(return_value=[Direction.EAST])
        pos = Position(1, 0)
        map.__get_or_create_node = MagicMock(return_value=Node(pos))

        assert (path.handle_discovery_finished() == Action.GO_EAST)

        # go north
        map.get_unvisited_directions = MagicMock(return_value=[Direction.EAST, Direction.NORTH])
        pos = Position(1, -1)
        map.__get_or_create_node = MagicMock(return_value=Node(pos))

        assert (path.handle_discovery_finished() == Action.GO_NORTH)

       # print(path.pathList)
        # return
        map.get_unvisited_directions = MagicMock(return_value=[])
        assert (path.handle_discovery_finished() == Action.GO_SOUTH)

    # print(path.pathList)

