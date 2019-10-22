from enum import Enum


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
    FINISHED = 3


class TurnEvents(Enum):
    NEW_ANGLE = 1


direction = {
    'L' : -90,
    'F' : 0,
    'R' : 90,
    'B' : 180
}


class DirectionController:
    def __init__(self):
        self._rawAngle = 0
        self._angleOffset = 0
        self._destinationAngle = 0
        self._lastColor = 'white'
        self._directionState = DirectionState.IDLE
        self._turnState = TurnState.IDLE
        self._name = 'direction controller'


    def discover(self, client, userdata, msg):
        print('discover')
        if self._directionState == DirectionState.IDLE:
            self.zeroAngle()
            self.processEvent(DirectionEvents.START_DISCOVERY, None)
        else:
            print('error: robot busy, discover not allowed')


    def turn(self, client, userdata, msg):
        print('turn')
        if self._directionState == DirectionState.IDLE:
            self.zeroAngle()
            self.processEvent(DirectionEvents.START_TURN, direction.get(userdata, None))
        else:
            print('error: robot busy, turn not allowed')


    def updateAngle(self, client, userdata, msg):
        print('new angle')
        self._rawAngle = userdata
        if self._turnState == TurnState.TURN_ANGLE & self.correctedAngle() == self._destinationAngle:
            self.processEvent(DirectionEvents.POS_REACHED)


    def updateColor(self, client, userdata, msg):
        print('new color')
        if userdata != self._lastColor:
            self._lastColor = userdata
            self.processEvent(DirectionEvents.NEW_COLOR)


    def processEvent(self, event, data):
        oldState = self._directionState

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
            print('nothing to do')
        # DISCOVERY
        elif self._directionState == DirectionState.START_DISCOVERY:
            if self._directionState != oldState:
                # entry action
                print('START_DISCOVERY, entry action')
            else:
                # recurring action
                print('START_DISCOVERY, recurring action')
        elif self._directionState == DirectionState.DISCOVERY:
            if self._directionState != oldState:
                # entry action
                print('DISCOVERY, entry action')
            else:
                # recurring action
                print('DISCOVERY, recurring action')
        elif self._directionState == DirectionState.DISCOVERY_FINISHED:
            if self._directionState != oldState:
                # entry action
                print('DISCOVERY_FINISHED, entry action')
            else:
                # recurring action
                print('DISCOVERY_FINISHED, recurring action')
        # TURN
        elif self._directionState == DirectionState.TURN_TO_POS:
            if self._directionState != oldState:
                # entry action
                print('TURN_TO_POS, entry action')
            else:
                # recurring action
                print('TURN_TO_POS, recurring action')
        elif self._directionState == DirectionState.TURN_FINISHED:
            if self._directionState != oldState:
                # entry action
                print('TURN_FINISHED, entry action')
            else:
                # recurring action
                print('TURN_FINISHED, recurring action')


    def zeroAngle(self):
        self._angleOffset = self._rawAngle


    def correctedAngle(self):
        return self._rawAngle - self._angleOffset


    def roundedAngle(self):
        return round((self._rawAngle - self._angleOffset) / 90) * 90