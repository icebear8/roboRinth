
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

def DirectionSortOrder(dir):
  if dir == RoboDirection.NORTH:
    return 1
  elif dir == RoboDirection.EAST:
    return 2
  elif dir == RoboDirection.SOUTH:
    return 3
  else:
    return 4