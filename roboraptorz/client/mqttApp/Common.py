
from enum import Enum

# Abstracted direction of the robot to be used between RoboDriver and App
class RoboDirection(Enum):
  NORTH = 1
  EAST = 2
  SOUTH = 3
  WEST = 4

class RoboStatus(Enum):
  IDLE = 1
  BUSY = 2
