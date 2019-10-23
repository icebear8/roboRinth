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
    lostLineSearchCrossingCenter = 6
    reachCrossing = 7
    readyToStartDrive = 8

class FollowLineMotorSpeed(enum.Enum):
    stop = 1
    crossingSpeed = 2
    lineSpeed = 3
    rotatingSpeed = 4

class followLine:
    SEARCH_ANGLE = 15
    SEARCH_ANGLE_START = 45
    SEARCH_WAIT_TIME = 0.8
    SEARCH_WAIT_TIME_START = 2.5
    SEARCH_SPEED = 5
    LINE_SPEED = 15
    CROSSING_SPEED = 25
    CROSSING_ANGLE = 185
    CROSSING_WAIT_TIME = 0.9

    __searchTimer = None
    #_searchAngleToUse = SEARCH_ANGLE_START
    #_searchWaitTimeToUse = SEARCH_WAIT_TIME_START

    def __init__(self):
        logger.warning("FollowLine Constructor ")
        self.currentState = FollowLineState.stopped

    def setClientAndRobo(self, client, roboName):
        self._client = client
        self._roboName = roboName

    def isLineColor(self,color):
        if color.startswith("B") or color.startswith("Y") or color.startswith("R"):
            return True
        else :
            return False

    def updateColor(self, msg):

        if self.currentState == FollowLineState.readyToStartDrive:
            if self.isLineColor(msg):
                self._searchAngleToUse = self.SEARCH_ANGLE
                self._searchWaitTimeToUse = self.SEARCH_WAIT_TIME

                self.currentState = FollowLineState.driving
                self.setMotorSpeed(FollowLineMotorSpeed.lineSpeed)
            else:
                self._searchAngleToUse = self.SEARCH_ANGLE_START
                self._searchWaitTimeToUse = self.SEARCH_WAIT_TIME_START

                self.currentState = FollowLineState.driving
                self.updateColor("WhiteFakeToStartSearch")

        if (self.currentState == FollowLineState.driving):
            if (msg.startswith("W")):
                logger.debug("got White while driving: Lost line")
                self.currentState = FollowLineState.lostLineSearchRight
                self.setMotorSpeed(FollowLineMotorSpeed.rotatingSpeed)
                if (self.__searchTimer):
                    self.__searchTimer.cancel()
                self.__searchTimer = threading.Timer(self._searchWaitTimeToUse, self.handleTurnFinished)
                self.__searchTimer.start()
                #threading.Timer(self._searchWaitTimeToUse, self.handleTurnFinished).start()
                logger.debug("startSearchRight")
                #self._client.publish(self._roboName+"/request/txt", "White, in Driving")

        if ((self.currentState == FollowLineState.lostLineSearchLeft) or (self.currentState == FollowLineState.lostLineSearchRight)):
            if (self.isLineColor(msg)):
                if (self.__searchTimer):
                    self.__searchTimer.cancel()
                self._searchAngleToUse = self.SEARCH_ANGLE
                self._searchWaitTimeToUse = self.SEARCH_WAIT_TIME
                logger.debug("got Black while lineSearch")
                #self._client.publish(self._roboName+"/request/txt", "Black, in LostLine")

                self.setMotorSpeed(FollowLineMotorSpeed.stop)
                self.setMotorSpeed(FollowLineMotorSpeed.lineSpeed)
                self.currentState = FollowLineState.driving

    def handleStartDriving(self, msg=None):
        self.currentState = FollowLineState.readyToStartDrive

    def handleTurnFinished(self):
        if (self.currentState == FollowLineState.lostLineSearchRight):
            steering, angle = self.convertAngle(-2 * self._searchAngleToUse)
            controlString = "{\"speed\":\""+str(self.SEARCH_SPEED)+"\",\"steering\":\"" + str(steering)+"\",\"angle\":\""+str(angle)+"\"""}"
            self._client.publish(self._roboName+"/request/steering/turn", controlString)
            self.currentState = FollowLineState.lostLineSearchLeft
            if (self.__searchTimer):
                self.__searchTimer.cancel()
            self.__searchTimer = threading.Timer(self._searchWaitTimeToUse * 2, self.handleTurnFinished)
            self.__searchTimer.start()
            logger.debug("startSearchLeft")
            logger.debug(controlString)

        elif (self.currentState == FollowLineState.lostLineSearchLeft):
            steering, angle = self.convertAngle(self._searchAngleToUse)
            controlString = "{\"speed\":\""+str(self.SEARCH_SPEED)+"\",\"steering\":\"" + str(steering)+"\",\"angle\":\""+str(angle)+"\"""}"
            self._client.publish(self._roboName+"/request/steering/turn", controlString)
            self.currentState = FollowLineState.lostLineSearchCenter
            if (self.__searchTimer):
                self.__searchTimer.cancel()
            self.__searchTimer = threading.Timer(self._searchWaitTimeToUse, self.handleTurnFinished)
            self.__searchTimer.start()
            logger.debug("startSearchCenter")
            logger.debug(controlString)
        elif (self.currentState == FollowLineState.lostLineSearchCenter):
            self.currentState = FollowLineState.lostLineSearchCrossingCenter
            logger.info("reach crossing")
            self.setMotorSpeed(FollowLineMotorSpeed.crossingSpeed)
            if (self.__searchTimer):
                self.__searchTimer.cancel()
            self.__searchTimer = threading.Timer(self.CROSSING_WAIT_TIME, self.handleTurnFinished)
            self.__searchTimer.start()

        elif (self.currentState == FollowLineState.lostLineSearchCrossingCenter):
            self.currentState = FollowLineState.reachCrossing
            logger.info("crossing reached")
            self._client.publish(self._roboName + '/notification/crossingReached')

    def setMotorSpeed(self, speed):
        if (speed == FollowLineMotorSpeed.stop):
            self._client.publish(self._roboName+"/request/steering/activate", "{\"speed\":\"0\",\"steering\":\"0\"}")
        elif (speed == FollowLineMotorSpeed.crossingSpeed):
            self._client.publish(self._roboName+"/request/steering/turn", "{\"speed\":\""+str(self.CROSSING_SPEED)+"\",\"steering\":\"0\",\"angle\":\""+str(self.CROSSING_ANGLE)+"\"}")
        elif (speed == FollowLineMotorSpeed.lineSpeed):
            self._client.publish(self._roboName+"/request/steering/activate", "{\"speed\":\""+str(self.LINE_SPEED)+"\",\"steering\":\"0\"}")
        elif (speed == FollowLineMotorSpeed.rotatingSpeed):
            steering, angle = self.convertAngle(self._searchAngleToUse)
            controlString = "{\"speed\":\""+str(self.SEARCH_SPEED)+"\",\"steering\":\"" + str(steering)+"\",\"angle\":\""+str(angle)+"\"""}"
            self._client.publish(self._roboName+"/request/steering/turn", controlString)
            logger.debug(controlString)
        return

    def convertAngle(self, desiredangle):
        steering = 100 if desiredangle > 0 else -100
        angle = abs(desiredangle) * 186/90
        return steering, angle