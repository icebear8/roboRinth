import asyncio
from control import Control
from graphmap import GraphMap
from mqttclient_simulator import MqttClientSimulator
from pathdiscovery import PathDiscovery
from websocket_server import WebSocketServer


def test_simulator():
    client = MqttClientSimulator(sleep_time=0.25)

    theMap = GraphMap()
    path = PathDiscovery(theMap)
    server = WebSocketServer()
    control = Control(theMap, client, path, server)

    client.register_crossing_reached(control.onHandleCrossingReached)
    client.register_available_directions(control.onHandleDiscoveryFinished)
    #client.register_crossing_reached(lambda: client.discover_directions())
    #client.register_available_directions(lambda directions: client.drive_direction(directions[0]))
    asyncio.get_event_loop().call_later(3, lambda: client.discover_directions())
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    test_simulator()
