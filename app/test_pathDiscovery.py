from unittest import TestCase
from unittest.mock import MagicMock
from app.map import Direction, Map, Position, Node
from app.Path import PathDiscovery, Action

class TestPathDiscovery(TestCase):
    def test_handleCrossingReached(self):
        map = Map()
        pos = Position(0,0)
        map.get_node = MagicMock(return_value = Node(pos))

        path = PathDiscovery(map)

        #go west
        map.get_unvisited_directions = MagicMock(return_value = [Direction.EAST])
        pos = Position(1,0)
        map.get_node = MagicMock(return_value = Node(pos))

        assert(path.handleCrossingReached() == Action.goEast)

        #go north
        map.get_unvisited_directions = MagicMock(return_value = [Direction.EAST, Direction.NORTH])
        pos = Position(1,-1)
        map.get_node = MagicMock(return_value = Node(pos))

        assert(path.handleCrossingReached() == Action.goNorth)

        print(path.pathList)
        #return
        map.get_unvisited_directions = MagicMock(return_value = [])
        assert(path.handleCrossingReached() == Action.goSouth)

       # print(path.pathList)

    def test_handleDiscoveryFinished(self):
        pass

