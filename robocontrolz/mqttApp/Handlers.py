
import logging

logger = logging.getLogger(__name__)

def handleGyro(client, userdata, msg):
  userdata['directionController'].updateAngle(client, userdata, msg)

def handleColor(client, userdata, msg):
  #logger.debug("Color:" + str(msg.payload.decode("utf-8")))
  userdata['followLine'].updateColor(msg.payload.decode("utf-8"))
  userdata['directionController'].updateColor(msg.payload.decode("utf-8"))

def handleStartDriving(client, userdata, msg):
  logger.debug("StartDrive: " + str(msg.payload.decode("utf-8")))
  userdata['directionController'].turn(msg.payload.decode("utf-8"))
  #userdata['followLine'].handleStartDriving(msg.payload.decode("utf-8"))

def handleInit(client, userdata, msg):
  userdata['directionController'].init()
