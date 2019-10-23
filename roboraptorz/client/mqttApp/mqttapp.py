#!/usr/bin/env python

import argparse
import logging
import sys
import time


from MqttClient import MqttClient

from Control import *
from MapMatcher import *
from RoboDriver import *
from websocket_server import *

logger = logging.getLogger(__name__)

client = None

def _initializeLogging(loglevel):
  numeric_level = getattr(logging, loglevel.upper(), None)
  if not isinstance(numeric_level, int):
    numeric_level = getattr(logging, INFO, None)

  logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=numeric_level)
  logging.Formatter.converter = time.gmtime

def main(argv):
  parser = argparse.ArgumentParser(description='RoboRinth Robot Explorer')
  parser.add_argument('--host', type=str, help='host of the mqtt broker to connect', default = "192.168.0.200")
  parser.add_argument('--port', type=int, default=1883, help='port of the mqtt broker to connect')
  parser.add_argument('--clientId', type=str, default="", help='MQTT client connection id')
  parser.add_argument('--log', type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO", help='Loglevel ')

  args = parser.parse_args()

  _initializeLogging(args.log)
  logger.debug("Main started")

  # Setup mqtt client
  client = MqttClient(args.host, args.port, args.clientId)
  client.startAsync()
  time.sleep(2)

  # Test code for MapMatcher
  roboName="roboraptorz-0"
  roboDriver=RoboDriver(roboName)
  client.subscribeTopics(roboName + '/notification/#')
  client.addMessageHandler(roboDriver.getMqttHandlerList())

  roboDriver.setMqttClient(client)

  mapMatcher=MapMatcher()
  mapMatcher.registerRobotDriver(roboName, roboDriver)

  robots={}
  robots[roboName]=Control(roboName, mapMatcher, roboDriver)
  robots[roboName].start()
  # End test code

  input("\n\nPress Enter to abort...\n\n")

  # Terminate
  client.stop()

  logger.debug("Terminate")

if __name__ == '__main__':
  main(sys.argv[1:])
