#!/usr/bin/env python

import logging
import time
from RoboDriver import RoboDriver
from MqttClient import MqttClient

logger = logging.getLogger(__name__)
client = None

def _initializeLogging(loglevel):
  numeric_level = getattr(logging, loglevel.upper(), None)
  if not isinstance(numeric_level, int):
    numeric_level = getattr(logging, DEBUG, None)

  logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=numeric_level)
  logging.Formatter.converter = time.gmtime

def onStatusMock(status):
    logger.debug("Status notification: "+str(status))

def onColorsMock(dirDict):
    logger.debug("Direction notification: "+str(dirDict))


def main():

    # print(myRoboDriver.getMqttHandlerList())
    print("Hallo")

    host = "192.168.0.200"
    port = 1883
    loglevel = "DEBUG"
    clientId = None

    _initializeLogging(loglevel)
    logger.debug("Main started")

    # Setup mqtt client
    client = MqttClient(host, port, clientId)
    client.startAsync()
    time.sleep(2)

    # setup RoboDriver
    myRoboDriver = RoboDriver("roboraptorz")
    myRoboDriver.onStatus = onStatusMock
    myRoboDriver.onColors = onColorsMock

    client.subscribeTopics("roboraptorz/notification/#")
    client.addMessageHandler(myRoboDriver.getMqttHandlerList())

    myRoboDriver.setMqttClient(client)

    # myRoboDriver.driveDirection()
    # print("DriveDirection sent")
    input("\n\nPress Enter to abort...\n\n")


    # Terminate
    client.stop()

    logger.debug("Terminate")

if __name__ == '__main__':
  main()
