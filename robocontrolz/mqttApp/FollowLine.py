import logging
import enum

logger = logging.getLogger(__name__)

class FollowLineState(enum.Enum):
    stopped = 1
    driving = 2
    lostLine = 3
    reachCrossing = 4

class FollowLineMotorSpeed(enum.Enum):
    stop = 1
    slow = 2
    fast = 3

class followLine:

    def __init__(self):
        logger.warning("FollowLine Constructor ")
        self.currentState = FollowLineState.stopped

    def setClientAndRobo(self, client, roboName):
        self._client = client
        self._roboName = roboName

    def updateColor(self, msg):
        if (self.currentState == FollowLineState.driving):
            if (msg.startswith("B")):
                logger.debug("got Black while driving")
            if (msg.startswith("W")):
                logger.info("reach crossing")
                self.motorSpeed(FollowLineMotorSpeed.slow)
        if (self.currentState == FollowLineState.reachCrossing):
            if (msg.startswith("W")):
                logger.debug("got Whilte while in crossing")
            if (msg.startswith("B")):
                self.motorSpeed(FollowLineMotorSpeed.stop)
                logger.debug("got Black while in crossing, stop")

    def handleStartDriving(self, msg):
        self.motorSpeed(FollowLineMotorSpeed.fast)

    def motorSpeed(self, speed):
        if (speed == FollowLineMotorSpeed.stop):
            self.currentState = FollowLineState.stopped
            self._client.publish(self._roboName+"/request/steering/activate", "{\"speed\":\"0\",\"steering\":\"0\"}")
            return
        elif (speed == FollowLineMotorSpeed.slow):
            self.currentState = FollowLineState.reachCrossing
            self._client.publish(self._roboName+"/request/steering/activate", "{\"speed\":\"3\",\"steering\":\"0\"}")
            return
        elif (speed == FollowLineMotorSpeed.fast):
            self.currentState = FollowLineState.driving
            self._client.publish(self._roboName+"/request/steering/activate", "{\"speed\":\"10\",\"steering\":\"0\"}")
            return
        return

    def handleMotorPosition(self, msg):
        return