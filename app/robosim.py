import asyncio
import json
import os

from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_0
from hbmqtt.session import ApplicationMessage

from position import Position
from direction import Direction

MQTT_BROKER_URI = 'mqtt://localhost'

TOPIC_REQUEST_DISCOVER_DIRECTIONS = 'robo-sim/request/discoverDirections'
TOPIC_REQUEST_DRIVE_DIRECTIONS = 'robo-sim/request/driveDirections'
TOPIC_NOTIFY_AVAILABLE_DIRECTIONS = 'robo-sim/notification/availableDirections'
TOPIC_NOTIFY_CROSSING_REACHED = 'robo-sim/notification/crossingReached'


class RoboSimulator:
    def __init__(self, sleep_time: float):
        self.sleep_time = sleep_time
        self.position = Position(0, 0)
        self.edges = []
        self.crossing_reached_handlers = []
        self.available_directions_handlers = []
        self.__load_file(os.path.dirname(__file__) + '/test_maze.txt')

        self.client = MQTTClient()

    async def run(self):
        handlers = {
            TOPIC_REQUEST_DRIVE_DIRECTIONS: self.drive_direction,
            TOPIC_REQUEST_DISCOVER_DIRECTIONS: self.discover_directions,
        }

        await self.client.connect(MQTT_BROKER_URI, True)
        print('Connected!')

        await self.client.subscribe([(topic, QOS_0) for topic in handlers.keys()])
        print('Subscribed!')

        while True:
            message = await self.client.deliver_message()
            await asyncio.sleep(self.sleep_time)
            await handlers[message.topic](message)

    async def discover_directions(self, message: ApplicationMessage):
        print('Discover Directions...')

        directions = set()
        for direction in Direction:
            next_pos = self.position.new_pos_in_direction(direction)
            for pos1, pos2 in self.edges:
                if pos1 == self.position and pos2 == next_pos or pos2 == self.position and pos1 == next_pos:
                    directions.add(direction)

        mapping = {
            Direction.NORTH: 'N',
            Direction.SOUTH: 'S',
            Direction.WEST: 'W',
            Direction.EAST: 'E',
        }
        payload = json.dumps([[mapping[direction], 'B'] for direction in directions]).encode('utf-8')
        await self.client.publish(TOPIC_NOTIFY_AVAILABLE_DIRECTIONS, payload)

    async def drive_direction(self, message: ApplicationMessage):
        payload = json.loads(message.data)
        print('Drive Direction: ' + payload[0])
        mapping = {
            'N': Direction.NORTH,
            'S': Direction.SOUTH,
            'W': Direction.WEST,
            'E': Direction.EAST,
        }
        direction = mapping[payload[0]]

        self.position = self.position.new_pos_in_direction(direction)
        print('  new position: {}:{}'.format(self.position.x, self.position.y))
        await self.client.publish(TOPIC_NOTIFY_CROSSING_REACHED, b'')

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


if __name__ == '__main__':
    client = RoboSimulator(sleep_time=0.25)
    asyncio.get_event_loop().create_task(client.run())
    asyncio.get_event_loop().run_forever()
