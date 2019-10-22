
import logging
import Map
import json
import MqttClient
logger = logging.getLogger(__name__)

class Msg:
  pass

_defaultHost="localhost"
_defaultPort=1883

class RobotForwarder(object):
  def __init__(self, notifyFunc, topicPrefix, robot):
    self._notify = notifyFunc
    self.topicPrefix = topicPrefix
    self.robot = robot
    self.robot.setNotifyCallback(self.notify)
    self._subscriptions = {
      topicPrefix + "/request/init":                  self.initHandler,
      topicPrefix + "/request/discoverDirections":    self.discoverHandler,
      topicPrefix + "/request/driveDirections":       self.driveHandler,
    }

    self._notifications = {
      "busy":                 topicPrefix + "/notification/busy",
      "availableDirections":  topicPrefix + "/notification/availableDirections",
      "crossingReached":      topicPrefix + "/notification/crossingReached",
      "error":                topicPrefix + "/notification/error",
    }

  def initHandler(self, client, userdata, msg):
    logger.debug("Got Init")
    # payload is empty
    self.robot.init()

  def discoverHandler(self, client, userdata, msg):
    logger.debug("Got discover")
    # payload is empty
    self.robot.discoverDirections()

  def driveHandler(self, client, userdata, msg):
    logger.debug("Got drive")
    data = json.loads(msg.payload)

    if len(data) > 1:
      logger.warn("driveHandler has too many items")
    self.robot.moveLocal(data[0])

  def notify(self, simpleTopic, msg):
    self._notify(self._notifications[simpleTopic], msg)

class MqttHandler(object):
  def __init__(self, host=_defaultHost, port=_defaultPort, mapFile="", clientId=None, topicPrefix=""):
    self._client = MqttClient.MqttClient(host, port, clientId)
    self.map = Map.Map()
    self.map.loadMap(mapFile)

    self.robotForwarders = []
    self._subscriptions = {}
    for i,robot in enumerate(self.map.getRobots()):
      forwarder = RobotForwarder(self.notify, topicPrefix+"-%i"%(i), robot)
      self.robotForwarders.append(forwarder)
      self._subscriptions.update(forwarder._subscriptions)

    # forward subscriptions to our client (will subscribe on connect)
    self._client._subscriptions = self._subscriptions

  def notify(self, topic, msg):
    self._client._notify(topic, msg)
    logger.debug("Sent: %s to %s",msg, self._notifications[simpleTopic])

if __name__ == "__main__":
  mqttHandler = MqttHandler("file")

  msg = Msg()
  msg.payload = "[\"N\",\"E\"]"

  mqttHandler.driveHandler("","",msg)