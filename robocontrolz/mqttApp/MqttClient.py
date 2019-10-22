
import logging
import random
import sys

import paho.mqtt.client as mqtt
from FollowLine import followLine

import Handlers as handler
from DirectionController import DirectionController

logger = logging.getLogger(__name__)

dirCtrl = DirectionController()
f = followLine()

_defaultHost="localhost"
_defaultPort=1883
_roboName = "robo-01"

mqttSubscriptions = [
  #_roboName+"/notification/#",
  _roboName+"/request/discover",
  _roboName+"/notification/color/name",
  _roboName+"/request/driveDirectionsRaw"
  "robo-01/notification/color/name",
  "robo-01/notification/gyro/angle",
  "robo-01/request/discoverDirections",
  "robo-01/request/driveDirectionsRaw"

]

mqttSubscriptionHandlers = {
  _roboName+"/notification/color/#":   handler.handleColor,
  _roboName+"/notification/gyro/#":    handler.handleGyro,
  _roboName+"/request/discover":     dirCtrl.discover,
  _roboName+"/notification/color/name":    handler.handleColor,
  _roboName+"/request/driveDirectionsRaw":    handler.handleStartDriving,
  #_roboName+"/request/motor/position":    handler.handleMotorPosition,
}

class MqttClient:
  def __init__(self, host=_defaultHost, port=_defaultPort, clientId=None):
    if clientId is None:
      clientId = "mqttapp_" + str(random.randint(1, sys.maxsize))

    logger.debug("Init client, host: " + str(host) + "; port: " + str(port) + "; clientId: " + clientId)

    self._host = host
    self._port = port
    self._keepalive = 60

    userdata.followLine = f
    userdata.directionContoller = dirCtrl
    self._client = mqtt.Client(client_id=clientId, clean_session=True, userdata=userdata)
    self._client.on_connect = self._onConnect
    self._client.on_subscribe = self._onSubscribe
    self._client.on_unsubscribe = self._onUnsubscribe
    self._client.on_disconnect = self._onDisconnect
    self._client.on_message = self._onMessage
    f.setClientAndRobo(self._client, _roboName)

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
    #client.publish(_roboName+"/subscribe/gyro/angle")
    self._client.publish(_roboName+"/subscribe/color/name")

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
