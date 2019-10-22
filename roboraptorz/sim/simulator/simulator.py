#!/usr/bin/env python

import argparse
import logging
import time
import sys
import threading
from MqttHandler import MqttHandler

logger = logging.getLogger(__name__)

running = True

def _initializeLogging(loglevel):
  numeric_level = getattr(logging, loglevel.upper(), None)
  if not isinstance(numeric_level, int):
    numeric_level = getattr(logging, INFO, None)

  logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=numeric_level)
  logging.Formatter.converter = time.gmtime

def mapPrinter(map):
  global running

  with open("map.txt", "w") as fd:
    while (running):
      lines = map.asciiDraw()
      for i in range(len(lines)):
        pass
        # move up characters
        fd.write("\033[F")
        fd.flush()

      for line in lines:
        fd.write("".join(line) + "\n")

      time.sleep(1)

def main():
  global running
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
  printerThread = threading.Thread(target=mapPrinter, args=[handler.map])
  printerThread.start()

  # block until we want to shut down
  input("\n\nPress Enter to abort...\n\n")
  running = False

  # Terminate
  printerThread.join()
  handler._client.stop()

  logger.debug("Terminate")

if __name__ == '__main__':
  main()
