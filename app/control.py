import asyncio
from typing import Tuple, List

from color import Color
from direction import Direction
from graphmap import GraphMap
from mqttclient import MqttClient
from pathdiscovery import Action, PathDiscovery
from websocket_server import WebSocketServer


class Control:
    def __init__(self, graph_map: GraphMap, mqtt_client: MqttClient, path: PathDiscovery, websocket_server: WebSocketServer):
        self.__graph_map = graph_map
        self.__mqtt_client = mqtt_client
        self.__path = path
        self.__websocket_server = websocket_server

        mqtt_client.register_crossing_reached(self.handle_crossing_reached)
        mqtt_client.register_available_directions(self.handle_discovery_finished)

    async def run(self):
        await asyncio.sleep(3)
        self.__mqtt_client.discover_directions()

    def handle_crossing_reached(self):
        print("onHandleCrossingReached")
        self.__websocket_server.send_update(self.__graph_map, self.__path.get_current_position())
        action = self.__path.handle_crossing_reached()
        self.handle_action(action)

    def handle_action(self, action: Action):
        if action == Action.DO_DISCOVERY:
            self.__mqtt_client.discover_directions()
        elif action == None:
            pass
        elif action == Action.DO_ABORT:
            print("I have seen the whole world. Roger an out!")
            asyncio.get_event_loop().stop()
        else:
            self.__mqtt_client.drive_directions([self.__path.convert_action_to_direction(action)])

    def handle_discovery_finished(self, directions: List[Tuple[Direction, Color]]):
        print("onHandleDiscoveryFinished:" + str(directions))
        self.__graph_map.node_discovered(self.__path.get_current_position(), directions)
        self.__websocket_server.send_update(self.__graph_map, self.__path.get_current_position())
        action = self.__path.handle_discovery_finished()
        self.handle_action(action)
