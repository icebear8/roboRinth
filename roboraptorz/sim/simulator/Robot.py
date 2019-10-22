import logging
import threading
from matrix import Matrix

logger = logging.getLogger(__name__)

class Robot(object):

    INIT_TIME_S = 2
    MOVING_TIME_S = 0.5
    DISCOVER_TIME_S = 0.5

    def __init__(self, map, globalPosition, rotLocToGlob, rotGlobToLoc):
        self.map = map
        self.globalPosition = globalPosition
        self.rotLocToGlob = rotLocToGlob
        self.rotGlobToLoc = rotGlobToLoc
        self._notify = None

    def makeAvailableDirectionsJson(self, listOfLists):
        strlist = [ "[\"" + "\",\"".join(item) + "\"]" for item in listOfLists]
        return  "[" + ",".join(strlist) + "]"

    def sendBusy(self):
        self.notify("busy","")

    def sendAvailableDirections(self, listOfLists):
        self.notify("availableDirections", self.makeAvailableDirectionsJson(listOfLists))

    def sendCrossingReached(self):
        self.notify("crossingReached","")

    def sendError(self, errorMsg):
        self.notify("error", errorMsg)

    def notify(self, topic, msg):
        if self._notify:
            self._notify(topic, msg)
        else:
            logger.warn("_notify callback not set!!")

    def setNotifyCallback(self, callback):
        self._notify = callback

    def init(self):
        logger.debug("Got Init")
        self.sendBusy()
        timer = threading.Timer(Robot.INIT_TIME_S, self.onInit)
        timer.start()

    def onInit(self):
        self.sendCrossingReached()

    def driveDirections(self, direction):
        logger.debug("Got drive Direction: %s"%(direction))
        self.sendBusy()
        v = Matrix._makeMatrix([[1], [0]])
        if direction == "N":
            v = Matrix._makeMatrix([[1], [0]])
        elif direction == "E":
            v = Matrix._makeMatrix([[0], [-1]])
        elif direction == "S":
            v = Matrix._makeMatrix([[-1], [0]])
        elif direction == "W":
            v = Matrix._makeMatrix([[0], [1]])

        if self.moveLocal(v):
            logger.debug("moving %s"%(direction))
            timer = threading.Timer(Robot.MOVING_TIME_S, self.onDriveDirections)
            timer.start()
        else:
            logger.warn("moving failed")
            self.sendError("Not a valid direction: %s"%(direction))

    def onDriveDirections(self):
        self.sendCrossingReached()

    def discoverDirections(self):
        logger.debug("Got discoverDirections")
        self.sendBusy()
        timer = threading.Timer(Robot.DISCOVER_TIME_S, self.onDisconverDirections)
        timer.start()

    def onDisconverDirections(self):
        self.sendAvailableDirections(self.scan())

    # Private: --------------------------------------------------
    def moveGlobal(self, direction):
        if self.map.isConnection(self.globalPosition, direction):
            self.globalPosition += direction
            return True
        return False

    def moveLocal(self, directionLocal):
        return self.moveGlobal(self.rotateLocalToGlobal(directionLocal))

    def rotateLocalToGlobal(self, direction):
        return self.rotLocToGlob*direction

    def rotateGlobalToLocal(self, direction):
        return self.rotGlobToLoc*direction

    def scan(self):
        v = []
        color = self.map.getColor(self.globalPosition, self.rotateLocalToGlobal(Matrix.fromList([[1], [0]])))
        if color:
            v.append(["N", color])
        color = self.map.getColor(self.globalPosition, self.rotateLocalToGlobal(Matrix.fromList([[0], [-1]])))
        if color:
            v.append(["E", color])
        color = self.map.getColor(self.globalPosition, self.rotateLocalToGlobal(Matrix.fromList([[-1], [0]])))
        if color:
            v.append(["S", color])
        color = self.map.getColor(self.globalPosition, self.rotateLocalToGlobal(Matrix.fromList([[0], [1]])))
        if color:
            v.append(["W", color])

        return v


if __name__ == "__main__":
    rotLocToGlob = Matrix._makeMatrix([[0, 1], [-1, 0]])
    rotGlobToLoc = Matrix._makeMatrix([[0, -1], [1, 0]])
    r = Robot(None, Matrix._makeMatrix([[0], [0]]), rotLocToGlob, rotGlobToLoc)
    m = Matrix.fromList([[1], [0]])
    print(r.rotateLocalToGlobal(m))

    #print(r.makeAvailableDirectionsJson([["N","B"],["E","B"]]))
    #print(r.makeAvailableDirectionsJson([]))
