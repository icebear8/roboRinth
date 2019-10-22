
import logging
import random
import sys
from direction import Direction
import json
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

_defaultHost="localhost"
_defaultPort=1883

mqttSubscriptions = [
  "robo-01/notification/CrossingReached/#",
  "robo-01/notification/DiscoveryFinished/#",
  "robo-01/notification/busy/#",
]
mqttSubscriptionHandlers = {
  "robo-01/notification/CrossingReached/#":   None,
  "robo-01/notification/DiscoveryFinished/#":    None,
  "robo-01/notification/busy/#":              None,
}

class MqttClient:
  def __init__(self, host=_defaultHost, port=_defaultPort, clientId=None):
    if clientId is None:
      clientId = "mqttapp_" + str(random.randint(1, sys.maxsize))

    logger.debug("Init client, host: " + str(host) + "; port: " + str(port) + "; clientId: " + clientId)

    mqttSubscriptionHandlers["robo-01/notification/CrossingReached/#"] = self._crossingReachedCallack
    mqttSubscriptionHandlers["robo-01/notification/DiscoveryFinished/#"] = self._discoveryFinishedCallback
    mqttSubscriptionHandlers["robo-01/notification/busy/#"] = self._robotIsBusyCallback

    self._host = host
    self._port = port
    self._keepalive = 60
    self._client = mqtt.Client(client_id=clientId, clean_session=True)
    self._client.on_connect = self._onConnect
    self._client.on_subscribe = self._onSubscribe
    self._client.on_unsubscribe = self._onUnsubscribe
    self._client.on_disconnect = self._onDisconnect
    self._client.on_message = self._onMessage
    self._crossingReachedHandlers = []
    self._discoveryFinishedHandlers = []
    self._roboIsBusyHandlers = []

  def subscribeCrossingReachedCallback(self,callback):
    self._crossingReachedHandlers.append(callback)

  def subscribeDiscoveryFinishedCallback(self,callback):
    self._discoveryFinishedHandlers.append(callback)

  def subscribeRoboIsBusyCallback(self,callback):
    self._roboIsBusyHandlers.append(callback)

  def startAsync(self):
    self._client.connect(self._host, self._port, self._keepalive)
    self._client.loop_start();

  def stop(self):
    self._client.loop_stop();
    self._client.disconnect()

  def _subscribeTopics(self, topics):
    for topic in topics:
      self._client.subscribe(topic)

  def _setupMessageHandler(self, handlers):
    for handler in handlers:
      self._client.message_callback_add(handler, handlers[handler])

  def _setupNotifications(self):
    logger.debug("SETUP")

  def subscribeMessage(self, topic, function):
    self._client.subscribe()

  def _onConnect(self, client, userdata, flags, rc):
    logger.debug("Connected with result code " + str(rc))
    self._subscribeTopics(mqttSubscriptions)
    self._setupMessageHandler(mqttSubscriptionHandlers)
    self._setupNotifications()

  def _onDisconnect(self, client, userdata, rc):
    if rc != 0:
      logger.warn("Unexpected disconnection")

  def _onSubscribe(self, client, userdata, mid, granted_qos):
    logger.debug("Subscribed " + str(mid))

  def _onUnsubscribe(self, client, userdata, mid, granted_qos):
    logger.debug("Unsubscribed " + str(mid))

  def _onMessage(self, client, userdata, msg):
    logger.debug("Unhandled message: " + msg.topic + " " + str(msg.payload))

  def publishMessageDriveDirection(self, direction):
    payload = json.dumps(self._convert_direction_to_payload(direction))
    self._client.publish("lemi-01/notification/driveDirection/", payload);

  def publishDiscoverDirections(self):
    self._client.publish("lemi-01/notification/discoverDirections/")

  def _crossingReachedCallack(self,client, userdata, msg):
    for callback in self._crossingReachedHandlers:
      callback()

  def _discoveryFinishedCallback(self,client, userdata, msg):
    logger.debug("_discoveryFinishedCallback") 
    avaiable_directories = self._convert_payload_to_directions(json.loads(msg.payload))
    for callback in self._discoveryFinishedHandlers:
      callback(avaiable_directories)

  def _robotIsBusyCallback(self,client, userdata, msg):
    for callback in self._roboIsBusyHandlers:
      callback()  

  def _convert_payload_to_directions(self, payload):
    mapping_direction = {"E":Direction.EAST, "N" : Direction.NORTH, "S" : Direction.SOUTH, "W" : Direction.WEST}
    mapping_color = {"E":Direction.EAST, "N" : Direction.NORTH, "S" : Direction.SOUTH, "W" : Direction.WEST}
    return [(mapping_direction[entry[0]], mapping_color[entry[1]]) for entry in payload]

  def _convert_direction_to_payload(self, directions):
    mapping_list = {Direction.EAST:"E", Direction.NORTH: "N", Direction.SOUTH : "S",Direction.WEST:"W"}
    return [mapping_list[entry] for entry in directions]

