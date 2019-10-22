from enum import IntEnum


class Direction(IntEnum):
    NORTH = 0,
    EAST = 1,
    SOUTH = 2,
    WEST = 3,

    def to_char(self):
        mapping = {
            Direction.NORTH: 'N',
            Direction.SOUTH: 'S',
            Direction.WEST: 'W',
            Direction.EAST: 'E',
        }
        return mapping[self]

    @staticmethod
    def from_char(char):
        mapping = {
            'N': Direction.NORTH,
            'S': Direction.SOUTH,
            'W': Direction.WEST,
            'E': Direction.EAST,
        }
        return mapping[char]
