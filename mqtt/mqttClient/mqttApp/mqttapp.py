#!/usr/bin/env python

import getopt
import logging
import random
import sys
import time

import paho.mqtt.client as mqtt

logger = logging.getLogger("MQTTapp")

_defaultHost="localhost"
_defaultPort=1883

client = None

def onConnect(client, userdata, flags, rc):
  logger.debug("Connected with result code " + str(rc))

def onMessage(client, userdata, msg):
    logger.debug("Recievied message" + msg.topic + " " + str(msg.payload))

def _initClient(host, port, clientId):
  global client

  logger.debug("Init client, host: " + str(host) + "; port: " + str(port) + "; clientId: " + clientId)

  client = mqtt.Client(client_id=clientId, clean_session=True)
  client.on_connect = onConnect
  client.onMessage = onMessage
  keepalive = 60
  client.connect(host, port, keepalive)

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

  host = _defaultHost
  port = _defaultPort
  loglevel = "DEBUG"
  clientId = "mqttapp_" + str(random.randint(1, sys.maxsize))

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
  _initClient(host, port, clientId)
  client.loop_start()
  time.sleep(2)

  input("Press Enter to abort...")

  # Terminate
  client.loop_stop()
  client.disconnect()

  logger.debug("Terminate")

if __name__ == '__main__':
  main(sys.argv[1:])
