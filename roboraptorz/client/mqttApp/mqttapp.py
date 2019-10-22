#!/usr/bin/env python

import getopt
import logging
import sys
import time

from MqttClient import MqttClient

from Control import *
from MapMatcher import *
from RoboDriver import *

logger = logging.getLogger(__name__)

client = None

def _mqttCallbackSim(driver, client, userdata, msg):
  logger.debug("_mqttCallbackSim topic: " + str(msg.topic) + " payload: " + str(msg.payload))
  incomming = msg.payload.decode('utf-8')
  logger.debug("_mqttCallbackSim incomming: " + incomming)

  directions = []

  if driver.onDirections is not None:

    if incomming in ('north'):
      directions.append(RoboDirection.NORTH)
    elif incomming in ('east'):
      directions.append(RoboDirection.EAST)
    elif incomming  in ('south'):
      directions.append(RoboDirection.SOUTH)
    elif incomming  in ('west'):
      directions.append(RoboDirection.WEST)

  logger.debug("_mqttCallbackSim directions: " + str(directions))
  driver.onDirections(directions)

def _initializeLogging(loglevel):
  numeric_level = getattr(logging, loglevel.upper(), None)
  if not isinstance(numeric_level, int):
    numeric_level = getattr(logging, INFO, None)

  logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=numeric_level)
  logging.Formatter.converter = time.gmtime

def _printUsage():
  print('mqttapp.py [--host=, --port=, --log=]')
  print('--host=: Host name or IP to connect')
  print('--port=: Port to connect')
  print('--clientId=: MQTT client connection id')
  print('--log=: Loglevel [DEBUG, INFO, WARNING, ERROR, CRITICAL]')

def main(argv):

  host = "localhost"
  port = 1883
  loglevel = "DEBUG"
  clientId = None

  # Readout arguments
  try:
    opts, args = getopt.getopt(argv, "h", ["help", "host=", "port=", "clientId=", "log="])
  except getopt.GetoptError as err:
    print(err)  # will print something like "option -a not recognized"
    _printUsage()
    sys.exit(2)

  for opt, arg in opts:
    if opt in ('-h', '--help'):
      _printUsage()
      sys.exit()
    elif opt in ('--host'):
      host = arg
    elif opt in ('--port'):
      try:
        port = int(arg)
      except ValueError:
        pass
    elif opt in ('--log='):
      loglevel = arg

  _initializeLogging(loglevel)
  logger.debug("Main started")

  # Setup mqtt client
  client = MqttClient(host, port, clientId)
  client.startAsync()
  time.sleep(2)

  # Test code for MapMatcher
  roboName="roboraptorz"
  roboDriver=RoboDriver(roboName)
  mapMatcher=MapMatcher()
  mapMatcher.registerRobotDriver(roboName, roboDriver)
  roboName=Control(roboName, mapMatcher, roboDriver)

  callback = lambda client, userdata, msg : _mqttCallbackSim(roboDriver, client, userdata, msg)
  simHandlers = {
    "roboraptorz/notification/availableDirectionsMapTest": callback
  }
  client.addMessageHandler(simHandlers)

  # End test code

  input("\n\nPress Enter to abort...\n\n")

  # Terminate
  client.stop()

  logger.debug("Terminate")

if __name__ == '__main__':
  main(sys.argv[1:])
