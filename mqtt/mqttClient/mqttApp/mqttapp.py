#!/usr/bin/env python

import logging
import sys
import time

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)
client = mqtt.Client()

def onConnect(client, userdata, flags, rc):
  logger.info("Connected with result code " + str(rc))

def _initClient(host, port):
  logger.info("Init client, host: " + host + "; port: " + port)
  client.on_connect = onConnect
  client.connect(host, port, 60)

def _clientLoop():
  client.loop_start()

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.INFO)
  logger.info("Main started")

  host="localhost"
  port=1883

  if len(sys.argv) >= 2:
    host=sys.argv[1]

  if len(sys.argv) >= 3:
    try:
      port = int(sys.argv[2])
    except ValueError:
      pass    # Nothing to do

  _initClient(host, port)
  _clientLoop()
