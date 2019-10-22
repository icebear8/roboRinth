import logging

from Common import *

logger = logging.getLogger(__name__)


# Supported Robodriver callbacks
# onStatus(status)
# onDirections(directions)
# onColors(directionColor))
class RoboDriver:
  def __init__(self, topicPrefix='robo-03'):
    self.onStatus=None
    self.onDirections=None
    self.onColors=None
    self._discoverMode=False
    self._status=RoboStatus.IDLE
    self._topicPrefix=topicPrefix
    self._mqttClient = None

  def _toDirEnum(self, dirString):
    if (dirString == 'N'):
      dirEnum = RoboDirection.NORTH
    elif (dirString == 'O'):
      dirEnum = RoboDirection.EAST
    elif (dirString == 'S'):
      dirEnum = RoboDirection.SOUTH
    elif (dirString == 'W'):
      dirEnum = RoboDirection.WEST

    return dirEnum

  def _toDirString(self,dirEnum):
    if (dirEnum == RoboDirection.NORTH):
      dirString = 'N'
    elif (dirEnum == RoboDirection.EAST):
      dirString = 'O'
    elif (dirEnum == RoboDirection.SOUTH):
      dirString = 'S'
    elif (dirEnum == RoboDirection.WEST):
      dirString = 'W'

    return dirString

  def setMqttClient(self, a_client):
    self._mqttClient = a_client

  def driveDirection(self, direction=RoboDirection.NORTH):
    if self._mqttClient is not None:
      # self._mqttClient.publish(self._topicPrefix+"/request/driveDirection", self._toDirString(direction))
      logger.debug("driveDirection: " + str(direction))

  def discoverMode(self, enabled=False):
    self._discoverMode=enabled
    logger.debug("discoverMode: " + str(self._discoverMode))

  def getDiscoverMode(self):
    return self._discoverMode

  def setDiscoverMode(self, mode):
    self._discoverMode = mode;

  def getStatus(self):
    return self._status

  # is called on mqtt Notifiction
  def mqtt_availDirection(self, client, user, msg):
    self._status = RoboStatus.IDLE
    logger.debug("Direction notification recieved")
    # TODO: evtl. check if correct topic
    dirDict = dict()
    for element in msg.payload:
      # TODO: string to direction enum
      dir[self._toDirEnum(element[0])] = element[1]


    # self.driveDirection(dirDict)
    logger.debug(dirDict)
    # self.onStatus(self._status)
    logger.debug(self._status)

  def mqtt_crossingReached(self):
    self._status = RoboStatus.IDLE
    logger.debug("crossingReached received")
    if self._discoverMode == True:
      # TODO: Start discovering
      logger.debug("blabla")
    else:
      # TODO:
      # self.onStatus(self._status)
      logger.debug(self._status)


  def mqtt_busy(self):
    self._status = RoboStatus.BUSY
    logger.debug("busyNotification recieved")

  def getMqttHandlerList(self):
    subscriberDict = {
      self._topicPrefix + "/notification/availableDirections/#": self.mqtt_availDirection,
      self._topicPrefix + "/notification/crossingReached/#": self.mqtt_crossingReached,
      self._topicPrefix + "/notification/busy/#": self.mqtt_busy
    }
    return subscriberDict
