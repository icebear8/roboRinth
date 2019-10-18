
import logging
import random
import sys

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

_defaultHost="localhost"
_defaultPort=1883

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
    self._client.on_message = self._onMessage

  def startAsync(self):
    self._client.connect(self._host, self._port, self._keepalive)
    self._client.loop_start();

  def stop(self):
    self._client.loop_stop();
    self._client.disconnect()

  def _onConnect(self, client, userdata, flags, rc):
    logger.debug("Connected with result code " + str(rc))

  def _onMessage(self, client, userdata, msg):
    logger.debug("Recievied message" + msg.topic + " " + str(msg.payload))
