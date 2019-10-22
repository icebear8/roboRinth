#!/usr/bin/env python

import getopt
import logging
import sys
import time

from MqttClient import MqttClient
from MqttClient import dirCtrl

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

  cmd = " "
  while cmd != "quit":

    cmd = input("\n\nEnter quit to abort\n\n")
    tokens = cmd.split(" ")
    if len(tokens) >= 1:
      if tokens[0] == "disco":
        client._client.publish("robo-01/request/discoverDirections")
      elif tokens[0] == "turn" and len(tokens) >= 2:
        client._client.publish("robo-01/request/driveDirectionsRaw", list(tokens[1]))
      elif tokens[0] == "reached":
        dirCtrl.posReached()
      elif tokens[0] == 'color' and len(tokens) >= 2:
        client._client.publish("robo-01/notification/color/name", tokens[1])
      elif tokens[0] == 'angle' and len(tokens) >= 2:
        client._client.publish("robo-01/notifiction/gyro/angle", tokens[1])

  # Terminate
  client.stop()

  logger.debug("Terminate")

if __name__ == '__main__':
  main(sys.argv[1:])
