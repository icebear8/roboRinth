import asyncio

from position import Position
from direction import Direction


class MqttClientSimulator:
    def __init__(self, sleep_time: int):
        self.sleep_time = sleep_time
        self.position = Position(1, 3)
        self.crossing_reached_handlers = []
        self.available_directions_handlers = []

        #   0   1   2   3
        #   *   *   *   *  0
        #       |
        #   * - * - *   *  1
        #       |   |
        #   *   * - *   *  2
        #       |
        #   *   *   *   *  3
        self.edges = [
            (Position(1, 3), Position(1, 2)),
            (Position(1, 2), Position(2, 2)),
            (Position(1, 2), Position(1, 1)),
            (Position(2, 2), Position(2, 1)),
            (Position(2, 1), Position(1, 1)),
            (Position(1, 1), Position(0, 1)),
            (Position(1, 1), Position(1, 0)),
            (Position(1, 1), Position(2, 1)),
        ]

    def discover_directions(self):
        directions = []
        for direction in Direction:
            next_pos = self.position.new_pos_in_direction(direction)
            for pos1, pos2 in self.edges:
                if pos1 == self.position and pos2 == next_pos or pos2 == self.position and pos1 == next_pos:
                    directions.append(direction)

        async def answer():
            await asyncio.sleep(self.sleep_time)
            for handler in self.available_directions_handlers:
                handler(directions)

        asyncio.get_event_loop().create_task(answer())

    def drive_direction(self, direction: Direction):
        self.position = self.position.new_pos_in_direction(direction)
        print('new position: {}/{}'.format(self.position.x, self.position.y))

        async def answer():
            await asyncio.sleep(self.sleep_time)
            for handler in self.crossing_reached_handlers:
                handler()

        asyncio.get_event_loop().create_task(answer())

    def register_crossing_reached(self, handler):
        self.crossing_reached_handlers.append(handler)

    def register_available_directions(self, handler):
        self.available_directions_handlers.append(handler)

