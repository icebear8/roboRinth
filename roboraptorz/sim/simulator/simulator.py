#!/usr/bin/env python

import argparse
import logging
import time

from MqttHandler import MqttHandler

logger = logging.getLogger(__name__)

client = None

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

def main():
  parser = argparse.ArgumentParser(description='RoboRinth Robot Simulator')
  parser.add_argument('--host', type=str, help='host of the mqtt broker to connect', default = "192.168.0.200")
  parser.add_argument('--port', type=int, default=1883, help='port of the mqtt broker to connect')
  parser.add_argument('--mapFile', type=str, default="default.map", help='port of the mqtt broker to connect')
  parser.add_argument('--clientId', type=str, default="", help='MQTT client connection id')
  parser.add_argument('--topicPrefix', type=str, default="roboraptorz", help="topic prefix for mqtt topics")
  parser.add_argument('--log', type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="DEBUG", help='Loglevel ')

  args = parser.parse_args()

  _initializeLogging(args.log)
  logger.debug("Main started")

  # Setup mqtt client
  handler = MqttHandler(args.host, args.port, args.mapFile, args.clientId, args.topicPrefix)

  handler._client.startAsync()
  time.sleep(2)

  input("\n\nPress Enter to abort...\n\n")

  # Terminate
  handler._client.stop()

  logger.debug("Terminate")

if __name__ == '__main__':
  main()
