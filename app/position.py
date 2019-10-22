from direction import Direction


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def new_pos_in_direction(self, direction: Direction, distance: int = 1) -> 'Position':
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

    def __repr__(self):
        return 'Position({}, {})'.format(self.x, self.y)