import asyncio
import json
import os

from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_0
from hbmqtt.session import ApplicationMessage

from color import Color
from mqttclient import TOPIC_REQUEST_DRIVE_DIRECTIONS, TOPIC_REQUEST_DISCOVER_DIRECTIONS, MQTT_BROKER_URI, \
    TOPIC_NOTIFY_AVAILABLE_DIRECTIONS, TOPIC_NOTIFY_CROSSING_REACHED
from position import Position
from direction import Direction


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

        result = []
        for direction in Direction:
            next_pos = self.position.new_pos_in_direction(direction)
            for pos1, pos2, color in self.edges:
                if pos1 == self.position and pos2 == next_pos or pos2 == self.position and pos1 == next_pos:
                    result.append((direction, color))

        payload = json.dumps([[direction.to_char(), color.to_char()] for direction, color in result]).encode('utf-8')
        await self.client.publish(TOPIC_NOTIFY_AVAILABLE_DIRECTIONS, payload)

    async def drive_direction(self, message: ApplicationMessage):
        payload = json.loads(message.data)
        print('Drive Direction: ' + payload[0])
        direction = Direction.from_char(payload[0])

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
                            Color.BLACK,
                        ))
                    if char == '|':
                        self.edges.append((
                            Position(int(col / 2), int((row - 1) / 2)),
                            Position(int(col / 2), int((row - 1) / 2) + 1),
                            Color.BLACK,
                        ))
                    if char == 'r':
                        if row % 2 == 0:
                            self.edges.append((
                                Position(int((col - 1) / 2), int(row / 2)),
                                Position(int((col - 1) / 2) + 1, int(row / 2)),
                                Color.BLACK,
                            ))
                        else:
                            self.edges.append((
                                Position(int(col / 2), int((row - 1) / 2)),
                                Position(int(col / 2), int((row - 1) / 2) + 1),
                                Color.RED,
                            ))

                    if char == 's':
                        self.position = Position(int(col / 2), int(row / 2))

