import asyncio
import os

from position import Position
from direction import Direction


class MqttClientSimulator:
    def __init__(self, sleep_time: float):
        self.sleep_time = sleep_time
        self.position = Position(0, 0)
        self.edges = []
        self.crossing_reached_handlers = []
        self.available_directions_handlers = []
        self.__load_file(os.path.dirname(__file__) + '/test_maze.txt')

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

    def __load_file(self, path: str):
        self.edges = []
        with open(path, 'r') as file:
            for row, line in enumerate(file.readlines()):
                for col, char in enumerate(line):
                    if char == '-':
                        self.edges.append((
                            Position(int((col - 1) / 2), int(row / 2)),
                            Position(int((col - 1) / 2) + 1, int(row / 2)),
                        ))
                    if char == '|':
                        self.edges.append((
                            Position(int(col / 2), int((row - 1) / 2)),
                            Position(int(col / 2), int((row - 1) / 2) + 1),
                        ))

                    if char == 's':
                        self.position = Position(int(col / 2), int(row / 2))
        for edge in self.edges:
            print(edge)
        print(self.position)
