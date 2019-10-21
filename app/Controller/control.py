
import logging
import random
import sys

logger = logging.getLogger(__name__)



class Control:
  def __init__(self, name):
    logger.debug("onHandleCrossingReached: " + str(name))

  def onHandleCrossingReached(self,client, userdata, msg):
    logger.debug("onHandleCrossingReached: " + msg.topic + " " + str(msg.payload))

  def onHandleDiscoveryFinished(self,client, userdata, msg):
    logger.debug("onHandleDiscoveryFinished: " + msg.topic + " " + str(msg.payload))


   
