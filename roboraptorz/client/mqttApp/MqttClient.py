
import logging
import random
import sys

import paho.mqtt.client as mqtt

import Handlers as handler

logger = logging.getLogger(__name__)

_defaultHost="localhost"
_defaultPort=1883

mqttSubscriptions = [
  # "robo-03/notification/#",
  "roboraptorz/notification/#",
]

mqttSubscriptionHandlers = {
  # "robo-03/notification/color/#":   handler.handleColor,
  # "robo-03/notification/gyro/#":    handler.handleGyro,
}

class MqttClient:
  def __init__(self, host=_defaultHost, port=_defaultPort, clientId=None):
    if clientId is None:
      clientId = "mqttapp_" + str(random.randint(1, sys.maxsize))

    logger.debug("Init client, host: " + str(host) + "; port: " + str(port) + "; clientId: " + clientId)

    self._host = host
    self._port = port
    self._keepalive = 60

    self._client = mqtt.Client(client_id=clientId, clean_session=True)
    self._client.on_connect = self._onConnect
    self._client.on_subscribe = self._onSubscribe
    self._client.on_unsubscribe = self._onUnsubscribe
    self._client.on_disconnect = self._onDisconnect
    # self._client.on_message = self._onMessage

  def startAsync(self):
    self._client.connect(self._host, self._port, self._keepalive)
    self._client.loop_start();

  def stop(self):
    self._client.loop_stop();
    self._client.disconnect()



  def publish(self, a_topic, a_payload, a_retain=False):
    self._client.publish(topic=a_topic,payload=a_payload,retain=a_retain)


  def subscribeTopics(self, topics):
    for topic in topics:
      self._client.subscribe(topic)

  def addMessageHandler(self, handlers):
    for handler in handlers:
      self._client.message_callback_add(handler, handlers[handler])

  def _setupNotifications(self):
    client.publish("robo-01/subscribe/color/name")
    client.publish("robo-01/subscribe/gyro/angle")

  def _onConnect(self, client, userdata, flags, rc):
    logger.debug("Connected with result code " + str(rc))
    self.subscribeTopics(mqttSubscriptions)
    self.addMessageHandler(mqttSubscriptionHandlers)
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
