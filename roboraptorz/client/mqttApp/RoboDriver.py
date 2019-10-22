import logging
import json
from Common import *

loggerDrv = logging.getLogger(__name__)


# Supported Robodriver callbacks
# onStatus(status)
# onDirections(directions)
# onColors(directionColor))
# onError(errorStr)
class RoboDriver:
    def __init__(self, topicPrefix='robo-03'):
      self.onStatus=None
      self.onDirections=None
      self.onColors=None
      self._discoverMode=True
      self._status=RoboStatus.BUSY
      self._topicPrefix=topicPrefix
      self._mqttClient = None
      loggerDrv.debug("RoboDriver start")

    def _toDirEnum(self, dirString):
      if (dirString == 'N'):
        dirEnum = RoboDirection.NORTH
      elif (dirString == 'E'):
        dirEnum = RoboDirection.EAST
      elif (dirString == 'S'):
        dirEnum = RoboDirection.SOUTH
      elif (dirString == 'W'):
        dirEnum = RoboDirection.WEST

      return dirEnum

    def _toDirString(self,dirEnum):
      if (dirEnum == RoboDirection.NORTH):
        dirString = "N"
      elif (dirEnum == RoboDirection.EAST):
        dirString = "E"
      elif (dirEnum == RoboDirection.SOUTH):
        dirString = "S"
      elif (dirEnum == RoboDirection.WEST):
        dirString = "W"

      return dirString

    def setMqttClient(self, a_client):
      self._mqttClient = a_client
      # send init
      loggerDrv.debug("send Init..")
      self._mqttClient.publish(self._topicPrefix+"/request/init")

    def driveDirection(self, direction=RoboDirection.NORTH):
      if self._mqttClient is not None:
        self._status = RoboStatus.BUSY
        payLoad = "[\"" + self._toDirString(direction) + "\"]"
        self._mqttClient.publish(self._topicPrefix+"/request/driveDirections",a_payload=payLoad)
        loggerDrv.debug("driveDirection: " + str(direction))

    def discoverMode(self, enabled=False):
      if self._status == RoboStatus.IDLE:
        self._discoverMode = enabled
        self._mqttClient.publish(self._topicPrefix + "/request/discoverDirections")
        loggerDrv.debug("discoverMode: " + str(self._discoverMode))
        return True
      else:
        loggerDrv.debug("switch to discoverMode not possible, Device is busy")
        return False

    def getDiscoverMode(self):
      return self._discoverMode

    def getStatus(self):
      return self._status

    # is called on mqtt Notifiction
    def mqtt_availDirection(self, client, user, msg):
      self._status = RoboStatus.IDLE
      loggerDrv.debug("Direction notification recieved")
      # TODO: evtl. check if correct topic
      dirDict = dict()
      loggerDrv.debug("Payload: "+msg.payload.decode("utf-8"))
      dirCol = json.loads(msg.payload.decode("utf-8"))
      for element in dirCol:
        # TODO: string to direction enum
        # loggerDrv.debug("element: "+ str(element))
        # loggerDrv.debug("element0: " + str(element[0]))
        # loggerDrv.debug("element1: " + str(element[1]))
        dirDict[self._toDirEnum(element[0])] = element[1]
      self.onColors(dirDict)
      loggerDrv.debug(dirDict)
      self.onStatus(self._status)
      loggerDrv.debug(self._status)

    def mqtt_crossingReached(self, client, user, msg):
      loggerDrv.debug("crossingReached received")
      if self._discoverMode == True:
        # TODO: Start discovering
        loggerDrv.debug("Detect Direction..")
        self._mqttClient.publish(self._topicPrefix + "/request/discoverDirections")
      else:
        self._status = RoboStatus.IDLE
        loggerDrv.debug(str(self._status))
        self.onStatus(self._status)

    def mqtt_busy(self, client, user, msg):
      print("Busy recieved")
      self._status = RoboStatus.BUSY
      self.onStatus(self._status)

    def getMqttHandlerList(self):
      loggerDrv.debug("Test")
      subscriberDict = {
        self._topicPrefix + "/notification/availableDirections/#": self.mqtt_availDirection,
        self._topicPrefix + "/notification/crossingReached/#": self.mqtt_crossingReached,
        self._topicPrefix + "/notification/busy/#": self.mqtt_busy
      }
      return subscriberDict
