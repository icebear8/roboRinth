
import logging

logger = logging.getLogger(__name__)

def handleColor(client, userdata, msg):
  logger.debug("Color: " + msg.topic + " " + str(msg.payload))

def handleGyro(client, userdata, msg):
  logger.debug("Gyro: " + msg.topic + " " + str(msg.payload))
