import asyncio
import json
from typing import List

from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_0
from hbmqtt.session import ApplicationMessage

from color import Color
from direction import Direction

MQTT_BROKER_URI = 'mqtt://localhost'

TOPIC_REQUEST_DISCOVER_DIRECTIONS = 'robo-sim/request/discoverDirections'
TOPIC_REQUEST_DRIVE_DIRECTIONS = 'robo-sim/request/driveDirections'
TOPIC_NOTIFY_AVAILABLE_DIRECTIONS = 'robo-sim/notification/availableDirections'
TOPIC_NOTIFY_CROSSING_REACHED = 'robo-sim/notification/crossingReached'


class MqttClient:
    def __init__(self):
        self.__crossing_reached_handlers = []
        self.__available_directions_handlers = []
        self.__client = MQTTClient()

    def register_crossing_reached(self, handler):
        self.__crossing_reached_handlers.append(handler)

    def register_available_directions(self, handler):
        self.__available_directions_handlers.append(handler)

    async def run(self):
        handlers = {
            TOPIC_NOTIFY_CROSSING_REACHED: self.__crossing_reached,
            TOPIC_NOTIFY_AVAILABLE_DIRECTIONS: self.__available_directions,
        }

        await self.__client.connect(MQTT_BROKER_URI, True)
        print('Connected!')

        await self.__client.subscribe([(topic, QOS_0) for topic in handlers.keys()])
        print('Subscribed!')

        while True:
            message = await self.__client.deliver_message()
            await handlers[message.topic](message)

    def discover_directions(self):
        asyncio.get_event_loop().create_task(self.__client.publish(TOPIC_REQUEST_DISCOVER_DIRECTIONS, b''))

    def drive_directions(self, directions: List[Direction]):
        mapping = {
            Direction.NORTH: 'N',
            Direction.SOUTH: 'S',
            Direction.WEST: 'W',
            Direction.EAST: 'E',
        }
        payload = json.dumps([mapping[direction] for direction in directions]).encode('utf-8')
        asyncio.get_event_loop().create_task(self.__client.publish(TOPIC_REQUEST_DRIVE_DIRECTIONS, payload))

    async def __crossing_reached(self, message: ApplicationMessage):
        for handler in self.__crossing_reached_handlers:
            handler()

    async def __available_directions(self, message: ApplicationMessage):
        mapping_direction = {
            'N': Direction.NORTH,
            'S': Direction.SOUTH,
            'W': Direction.WEST,
            'E': Direction.EAST,
        }
        mapping_color = {
            'B': Color.BLACK,
            'R': Color.RED,
            'Y': Color.YELLOW,
        }
        directions = set([(mapping_direction[entry[0]], mapping_color[entry[1]]) for entry in json.loads(message.data)])

        for handler in self.__available_directions_handlers:
            handler(directions)
