import asyncio
from control import Control
from Path import PathDiscovery
from map import Map
from mqttclient_simulator import MqttClientSimulator
from Path import PathDiscovery

def test_simulator():
    client = MqttClientSimulator(sleep_time=1)

    theMap = Map()
    path = PathDiscovery(theMap)
    control = Control(theMap,client,path)

    client.register_crossing_reached(control.onHandleCrossingReached)
    client.register_available_directions(control.onHandleDiscoveryFinished)
    #client.register_crossing_reached(lambda: client.discover_directions())
    #client.register_available_directions(lambda directions: client.drive_direction(directions[0]))
    asyncio.get_event_loop().call_soon(lambda: client.discover_directions())
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    test_simulator()
