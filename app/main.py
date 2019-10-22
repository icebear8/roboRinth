import asyncio
from control import Control
from graphmap import GraphMap
from mqttclient import MqttClient
from pathdiscovery import PathDiscovery
from robosim import RoboSimulator
from websocket_server import WebSocketServer


def main():
    robosim = RoboSimulator(sleep_time=0.25)
    mqtt_client = MqttClient()
    websocket_server = WebSocketServer()
    graph_map = GraphMap()
    path = PathDiscovery(graph_map)
    control = Control(graph_map, mqtt_client, path, websocket_server)

    asyncio.get_event_loop().create_task(robosim.run())
    asyncio.get_event_loop().create_task(mqtt_client.run())
    asyncio.get_event_loop().create_task(control.run())
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
