import asyncio

from mqttclient_simulator import MqttClientSimulator


def test_simulator():
    client = MqttClientSimulator(sleep_time=1)
    client.register_crossing_reached(lambda: client.discover_directions())
    client.register_available_directions(lambda directions: client.drive_direction(directions[0]))
    asyncio.get_event_loop().call_soon(lambda: client.discover_directions())
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    test_simulator()
