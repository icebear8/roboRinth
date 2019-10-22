import logging
import enum
import threading
import time


logger = logging.getLogger(__name__)

class FollowLineState(enum.Enum):
    stopped = 1
    driving = 2
    lostLineSearchRight = 3
    lostLineSearchLeft = 4
    lostLineSearchCenter = 5
    reachCrossing = 6

class FollowLineMotorSpeed(enum.Enum):
    stop = 1
    crossingSpeed = 2
    lineSpeed = 3
    rotatingSpeed = 4

class followLine:
    searchAngle = 20
    waitTime = 2

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
                #self._client.publish(self._roboName+"/request/txt", "Black, in Driving")
            if (msg.startswith("W")):
                logger.debug("got White while driving: Lost line")
                self.currentState = FollowLineState.lostLineSearchRight
                self.setMotorSpeed(FollowLineMotorSpeed.rotatingSpeed)
                threading.Timer(self.waitTime, self.handleTurnFinished).start()
                logger.debug("startSearchRight")
                #self._client.publish(self._roboName+"/request/txt", "White, in Driving")

        if ((self.currentState == FollowLineState.lostLineSearchLeft) or (self.currentState == FollowLineState.lostLineSearchRight)):
            if (msg.startswith("B")):
                logger.debug("got Black while lineSearch")
                #self._client.publish(self._roboName+"/request/txt", "Black, in LostLine")

                self.setMotorSpeed(FollowLineMotorSpeed.stop)
                self.setMotorSpeed(FollowLineMotorSpeed.lineSpeed)
                self.currentState = FollowLineState.driving
        if (self.currentState == FollowLineState.reachCrossing):
            if (msg.startswith("W")):
                logger.debug("got Whilte while in crossing")
                #self._client.publish(self._roboName+"/request/txt", "White, in Crossing")

    def handleStartDriving(self, msg):
        self.setMotorSpeed(FollowLineMotorSpeed.lineSpeed)
        self.currentState = FollowLineState.driving

    def handleTurnFinished(self):
        if (self.currentState == FollowLineState.lostLineSearchRight):
            steering, angle = self.convertAngle(-2 * self.searchAngle)
            controlString = "{\"speed\":\"3\",\"steering\":\"" + str(steering)+"\",\"angle\":\""+str(angle)+"\"""}"
            self._client.publish(self._roboName+"/request/steering/turn", controlString)
            self.currentState = FollowLineState.lostLineSearchLeft
            threading.Timer(self.waitTime*2, self.handleTurnFinished).start()
            logger.debug("startSearchLeft")
            logger.debug(controlString)

        elif (self.currentState == FollowLineState.lostLineSearchLeft):
            steering, angle = self.convertAngle(self.searchAngle)
            controlString = "{\"speed\":\"3\",\"steering\":\"" + str(steering)+"\",\"angle\":\""+str(angle)+"\"""}"
            self._client.publish(self._roboName+"/request/steering/turn", controlString)
            self.currentState = FollowLineState.lostLineSearchCenter
            threading.Timer(self.waitTime, self.handleTurnFinished).start()
            logger.debug("startSearchCenter")
            logger.debug(controlString)
        elif (self.currentState == FollowLineState.lostLineSearchCenter):
            self.currentState = FollowLineState.reachCrossing
            logger.info("reach crossing")
            self.setMotorSpeed(FollowLineMotorSpeed.crossingSpeed)


    def setMotorSpeed(self, speed):
        if (speed == FollowLineMotorSpeed.stop):
            self._client.publish(self._roboName+"/request/steering/activate", "{\"speed\":\"0\",\"steering\":\"0\"}")
        elif (speed == FollowLineMotorSpeed.crossingSpeed):
            self._client.publish(self._roboName+"/request/steering/turn", "{\"speed\":\"30\",\"steering\":\"0\",\"angle\":\"250\"}")
        elif (speed == FollowLineMotorSpeed.lineSpeed):
            self._client.publish(self._roboName+"/request/steering/activate", "{\"speed\":\"10\",\"steering\":\"0\"}")
        elif (speed == FollowLineMotorSpeed.rotatingSpeed):
            steering, angle = self.convertAngle(self.searchAngle)
            controlString = "{\"speed\":\"3\",\"steering\":\"" + str(steering)+"\",\"angle\":\""+str(angle)+"\"""}"
            self._client.publish(self._roboName+"/request/steering/turn", controlString)
            logger.debug(controlString)
        return

    def handleMotorPosition(self, msg):
        return

    def convertAngle(self, desiredangle):
        steering = 100 if desiredangle > 0 else -100
        angle = abs(desiredangle) * 186/90
        return steering, angle