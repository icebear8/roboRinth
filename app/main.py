import asyncio
from control import Control
from graphmap import GraphMap
from mqttclient import MqttClient
from pathdiscovery import PathDiscovery
from websocket_server import WebSocketServer


def main():
    mqtt_client = MqttClient()
    websocket_server = WebSocketServer()
    graph_map = GraphMap()
    path = PathDiscovery(graph_map)
    control = Control(graph_map, mqtt_client, path, websocket_server)

    asyncio.get_event_loop().create_task(mqtt_client.run())
    asyncio.get_event_loop().create_task(control.run())
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
