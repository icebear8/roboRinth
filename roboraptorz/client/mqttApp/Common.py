
from enum import Enum

class ControlMode(Enum):
  SCOUTING = 1
  NAVIGATING = 2

# Abstracted direction of the robot to be used between RoboDriver and App
class RoboDirection(Enum):
  NORTH = 1
  EAST = 2
  SOUTH = 3
  WEST = 4

class RoboStatus(Enum):
  IDLE = 1
  BUSY = 2

class LineColor(Enum):
  Black = 1
  Yellow = 2
  Red = 3

def LineColorToStr(lineColor):
  if lineColor == LineColor.Black:
    return "Black"
  elif lineColor == LineColor.Red:
    return "Red"
  else:
    return "Yellow"

def DirectionSortOrder(dir):
  if dir == RoboDirection.NORTH:
    return 1
  elif dir == RoboDirection.EAST:
    return 2
  elif dir == RoboDirection.SOUTH:
    return 3
  else:
    return 4

def DirToStr(dir):
  if dir == RoboDirection.NORTH:
    return "NORTH"
  elif dir == RoboDirection.EAST:
    return "EAST"
  elif dir == RoboDirection.SOUTH:
    return "SOUTH"
  else:
    return "WEST"
