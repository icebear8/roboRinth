
import logging

logger = logging.getLogger(__name__)

def handleGyro(client, userdata, msg):
  logger.debug("Gyro: " + msg.topic + " " + str(msg.payload.decode("utf-8")))

def handleColor(client, userdata, msg):
  #logger.debug("Color:" + str(msg.payload.decode("utf-8")))
  userdata.updateColor(msg.payload.decode("utf-8"))

def handleStartDriving(client, userdata, msg):
  logger.debug("StartDrive: " + str(msg.payload.decode("utf-8")))
  userdata.handleStartDriving(msg.payload.decode("utf-8"))

def handleMotorPosition(client, userdata, msg):
  logger.debug("MotorPosition:" + msg.topic + " " + str(msg.payload.decode("utf-8")))
  userdata.updateMotorPosition()

