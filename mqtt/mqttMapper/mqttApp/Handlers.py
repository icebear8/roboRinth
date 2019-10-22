import json
import logging

logger = logging.getLogger(__name__)

orientation = dict()

orientations = ['N', 'E', 'S', 'W']
directions = ['F', 'R', 'B', 'L']


def symbolicOrientationFrom(robo, value):
    return orientations[(value + orientation[robo]) % 4]


def symbolicDirectionFrom(robo, value):
    return directions[(value - orientation[robo]) % 4]


def updateOrientationWithDirection(robo, direction):
    global orientation
    orientation[robo] = (orientation[robo] + directions.index(direction)) % 4
    return direction


def valueFromOrientation(symbol):
    return orientations.index(symbol)


def valueFromDirection(symbol):
    return directions.index(symbol)


def availableDirectionsRaw(client, userdata, msg):
    logger.debug("availableDirectionsRaw: " + msg.topic + " " + str(msg.payload))
    try:
        robo = msg.topic.split("/")[0]
        decoded = json.loads(msg.payload)
        client.publish(msg.topic[:-3],
                       json.dumps(
                           [(symbolicOrientationFrom(robo, valueFromDirection(d)), c) for (d, c)
                            in decoded]))
    except:
        client.publish(msg.topic[:-22] + "error", json.dumps("Invalid payload " + str(msg.payload) + " for topic " + msg.topic))


def driveDirections(client, userdata, msg):
    logger.debug("driveDirection: " + msg.topic + " " + str(msg.payload))
    try:
        robo = msg.topic.split("/")[0]
        payload = json.loads(msg.payload)
        client.publish(msg.topic + "Raw",
                       json.dumps([updateOrientationWithDirection(robo, symbolicDirectionFrom(robo, valueFromOrientation(d))) for d in payload]))
    except:
        client.publish(msg.topic[:-15] + "error", json.dumps("Invalid payload " + str(msg.payload) + " for topic " + msg.topic))

def init(client, userdata, msg):
    global orientation
    logger.debug("init: " + msg.topic + " " + str(msg.payload))
    robo = msg.topic.split("/")[0]
    orientation[robo] = 0
