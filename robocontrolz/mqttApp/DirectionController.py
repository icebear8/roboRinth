from enum import Enum

import json
import threading
import time


class DirectionState(Enum):
    IDLE = 1
    # DISCOVERY
    START_DISCOVERY = 2
    DISCOVERY = 3
    DISCOVERY_FINISHED = 4
    # TURN TO POSITION
    TURN_TO_POS = 5
    TURN_FINISHED = 6

class DirectionEvents(Enum):
    START_DISCOVERY = 1
    POS_REACHED = 2
    START_TURN = 3
    NEW_COLOR = 4

class TurnState(Enum):
    IDLE = 1
    TURN_ANGLE = 2

class TurnEvents(Enum):
    NEW_ANGLE = 1
    ANGLE_REACHED = 2

class DirectionController:
    SEARCH_SPEED = 10
    TURN_SPEED = 15
    TIMEOUT_CONST = 100 #75
    COLORS_MAP = {
        'Black': 'B',
        'Yellow': 'Y',
        'Red': 'R',
    }
    DIRECTION_TO_ANGLE_MAP = {
        'L': -90,
        'F': 0,
        'R': 90,
        'B': 180,
    }
    ANGLE_TO_DIRECTION_MAP = {
        0: 'F',
        90: 'R',
        180: 'B',
        270: 'L',
        360: 'F',
    }

    __searchTimer = None

    def __init__(self, followLine):
        self._followLine = followLine
        self._rawAngle = 0
        self._angleOffset = 0
        self._destinationAngle = 0
        self._lastColor = 'White'
        self._directionColorMap = {}
        self._directionState = DirectionState.IDLE
        self._turnState = TurnState.IDLE
        self._name = 'direction controller'

    def setClientAndRobo(self, client, roboName):
        self._mqtt = client
        self._roboName = roboName

    def init(self):
        print('init')
        parameters = dict()
        parameters['speed'] = 0
        parameters['steering'] = 0
        self._mqtt.publish(self._roboName + '/request/steering/activate', json.dumps(parameters))
        self._directionState = DirectionState.IDLE
        self._turnState = TurnState.IDLE
        self._mqtt.publish(self._roboName + '/notification/crossingReached')

    def discover(self, client, userdata, msg):
        print('discover')
        if self._directionState == DirectionState.IDLE:
            self.zeroAngle()
            self.processEvent(DirectionEvents.START_DISCOVERY, None)
        else:
            print('error: robot busy, discover not allowed')

    def turn(self, msg):
        if msg is None:
            return
        jdata = json.loads(msg)
        print('turn ' + str(jdata[0]))
        if self._directionState == DirectionState.IDLE:
            if type(jdata[0]) == int:
                self.processEvent(DirectionEvents.START_TURN, jdata[0])
            else:
                self.processEvent(DirectionEvents.START_TURN, self.DIRECTION_TO_ANGLE_MAP.get(jdata[0], 0))
        else:
            print('error: robot busy, turn not allowed')

    def updateAngle(self, client, userdata, msg):
        self._rawAngle = int(msg.payload.decode("utf-8"))

    def updateColor(self, msg):
        if msg != self._lastColor:
            self._lastColor = msg
            if msg in self.COLORS_MAP:
                self.processEvent(DirectionEvents.NEW_COLOR, msg)

    def processEvent(self, event, data=None):
        oldDirectionState = self._directionState

        # transitions
        # IDLE
        if self._directionState == DirectionState.IDLE:
            if event == DirectionEvents.START_DISCOVERY:
                self._directionState = DirectionState.START_DISCOVERY

            elif event == DirectionEvents.START_TURN:
                self._directionState = DirectionState.TURN_TO_POS

        # DISCOVERY
        elif self._directionState == DirectionState.START_DISCOVERY:
            if event == DirectionEvents.POS_REACHED:
                self._directionState = DirectionState.DISCOVERY

        elif self._directionState == DirectionState.DISCOVERY:
            if event == DirectionEvents.POS_REACHED:
                self._directionState = DirectionState.DISCOVERY_FINISHED

        elif self._directionState == DirectionState.DISCOVERY_FINISHED:
            self._directionState = DirectionState.IDLE

        # TURN
        elif self._directionState == DirectionState.TURN_TO_POS:
            if event == DirectionEvents.POS_REACHED:
                self._directionState = DirectionState.TURN_FINISHED

        elif self._directionState == DirectionState.TURN_FINISHED:
            self._directionState = DirectionState.IDLE

        # actions
        # IDLE
        if self._directionState == DirectionState.IDLE:
            if self._directionState != oldDirectionState:
                # entry action
                print('IDLE, nothing to do')
        # DISCOVERY
        elif self._directionState == DirectionState.START_DISCOVERY:
            if self._directionState != oldDirectionState:
                # entry action
                print('START_DISCOVERY, entry action')
                self._mqtt.publish(self._roboName + '/notification/busy')
                self.processTurnEvent(TurnEvents.NEW_ANGLE, -20)
            else:
                # recurring action
                print('START_DISCOVERY, recurring action')
        elif self._directionState == DirectionState.DISCOVERY:
            if self._directionState != oldDirectionState:
                # entry action
                print('DISCOVERY, entry action')
                self.processTurnEvent(TurnEvents.NEW_ANGLE, 380)
            else:
                # recurring action
                print('DISCOVERY, recurring action')
                print('add color to list: ' + self.ANGLE_TO_DIRECTION_MAP[self.roundedAngle()] + ', ' + self.COLORS_MAP[data])
                self._directionColorMap[self.ANGLE_TO_DIRECTION_MAP[self.roundedAngle()]] = self.COLORS_MAP[data]

        elif self._directionState == DirectionState.DISCOVERY_FINISHED:
            if self._directionState != oldDirectionState:
                # entry action
                print('DISCOVERY_FINISHED, entry action')
                self._mqtt.publish(self._roboName + '/notification/availableDirectionsRaw', self.dirMapToList(self._directionColorMap))
                self._directionColorMap = {}
                self.processEvent(None)
            else:
                # recurring action
                print('DISCOVERY_FINISHED, recurring action')
        # TURN
        elif self._directionState == DirectionState.TURN_TO_POS:
            if self._directionState != oldDirectionState:
                # entry action
                print('TURN_TO_POS, entry action')
                self._mqtt.publish(self._roboName + '/notification/busy')
                self.processTurnEvent(TurnEvents.NEW_ANGLE, data)
            else:
                # recurring action
                print('TURN_TO_POS, recurring action')
        elif self._directionState == DirectionState.TURN_FINISHED:
            if self._directionState != oldDirectionState:
                # entry action
                print('TURN_FINISHED, entry action')
                self._followLine.handleStartDriving()
                self.processEvent(None)
            else:
                # recurring action
                print('TURN_FINISHED, recurring action')

    def processTurnEvent(self, event, data=None):
        if self._turnState == TurnState.IDLE:
            if event == TurnEvents.NEW_ANGLE:
                print('start turn robot')
                self._destinationAngle = data
                steering, angle = self.convertAngle(data)
                parameters = dict()
                parameters['speed'] = self.SEARCH_SPEED
                parameters['steering'] = steering
                parameters['angle'] = angle
                self._mqtt.publish(self._roboName + '/request/steering/turn', json.dumps(parameters))
                self.startTimer(self.TIMEOUT_CONST/self.SEARCH_SPEED/360*abs(data))
                self._turnState = TurnState.TURN_ANGLE
        elif self._turnState == TurnState.TURN_ANGLE:
            if event == TurnEvents.ANGLE_REACHED:
                print('stop turn robot')
                self._turnState = TurnState.IDLE
                self.processEvent(DirectionEvents.POS_REACHED)

    def startTimer(self, time):
        if (self.__searchTimer):
            self.__searchTimer.cancel()
        self.__searchTimer = threading.Timer(time, self.onStopTimer)
        self.__searchTimer.start()

    def onStopTimer(self):
        self.processTurnEvent(TurnEvents.ANGLE_REACHED)

    def zeroAngle(self):
        self._angleOffset = self._rawAngle

    def convertAngle(self, desiredangle):
        steering = 100 if desiredangle > 0 else -100
        angle = abs(desiredangle) * 195/90
        return steering, angle

    def roundedAngle(self):
        return round((self._rawAngle - self._angleOffset) / 90) * 90

    def dirMapToList(self, dirMap):
        dirList = list()
        for key, value in dirMap.items():
            entry = [key, value]
            dirList.append(entry)
        return json.dumps(dirList)