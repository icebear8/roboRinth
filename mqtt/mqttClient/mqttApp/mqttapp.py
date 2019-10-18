#!/usr/bin/env python

import getopt
import logging
import sys
import time

import paho.mqtt.client as mqtt

logger = logging.getLogger("MQTTapp")

_defaultHost="mqtt.arctic"
_defaultPort=1883

client = mqtt.Client(client_id="testClient", clean_session=True)
def onConnect(client, userdata, flags, rc):
  logger.info("Connected with result code " + str(rc))

def _initClient(host, port):
  logger.info("Init client, host: " + host + "; port: " + port)
  client.on_connect = onConnect
  client.connect(host, port, 60)

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
  print('--log=: Loglevel [DEBUG, INFO, WARNING, ERROR, CRITICAL]')

def main(argv):

  host = _defaultHost
  port = _defaultPort
  loglevel = "INFO"

  # Readout arguments
  try:
    opts, args = getopt.getopt(argv, "h", ["help", "host=", "port=", "log="])
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
  logger.info("Main started")

  # Setup mqtt client
  _initClient(host, port)
  client.loop_start()

  logger.info("Terminate")

if __name__ == '__main__':
  main(sys.argv[1:])
