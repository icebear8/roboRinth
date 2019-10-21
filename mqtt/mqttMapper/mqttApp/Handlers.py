import json
import logging

logger = logging.getLogger(__name__)

orientation = 0

orientations = ['N', 'E', 'S', 'W']
directions = ['F', 'R', 'B', 'L']


def symbolicOrientationFrom(value):
    return orientations[(value + orientation) % 4]


def symbolicDirectionFrom(value):
    return directions[(value - orientation) % 4]


def updateOrientationWithDirection(direction):
    global orientation
    orientation = (orientation + directions.index(direction)) % 4
    return direction


def valueFromOrientation(symbol):
    return orientations.index(symbol)


def valueFromDirection(symbol):
    return directions.index(symbol)


def availableDirectionsRaw(client, userdata, msg):
    logger.debug("availableDirections: " + msg.topic + " " + str(msg.payload))
    client.publish(msg.topic[:-3],
                   json.dumps(
                       [(symbolicOrientationFrom(valueFromDirection(d)), c) for (d, c)
                        in json.loads(msg.payload)]))


def driveDirections(client, userdata, msg):
    logger.debug("driveDirection: " + msg.topic + " " + str(msg.payload))
    payload = json.loads(msg.payload)
    client.publish(msg.topic + "Raw",
                   json.dumps([updateOrientationWithDirection(symbolicDirectionFrom(valueFromOrientation(d))) for d in payload]))


def init(client, userdata, msg):
    global orientation
    logger.debug("init: " + msg.topic + " " + str(msg.payload))
    orientation = 0
