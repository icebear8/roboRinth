from RoboDriver import RoboDriver

def main():
    myRoboDriver = RoboDriver("robo04")
    print(myRoboDriver.getMqttHandlerList())
    print("Hallo")


if __name__ == '__main__':
  main()
