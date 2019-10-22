import getopt
import logging
import time
import sys

from MqttClient import MqttClient

logger = logging.getLogger(__name__)

client = None

def _initializeLogging(loglevel):
  numeric_level = getattr(logging, loglevel.upper(), None)
  if not isinstance(numeric_level, int):
    numeric_level = getattr(logging, DEBUG, None)

  logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=numeric_level)
  logging.Formatter.converter = time.gmtime

def main(argv):

  host = "192.168.0.200"
  port = 1883
  loglevel = "DEBUG"
  clientId = None

  # Readout arguments
  try:
    opts, args = getopt.getopt(argv, "h", ["help", "host=", "port=", "clientId=", "log="])
  except getopt.GetoptError as err:
    print(err)  # will print something like "option -a not recognized"
    _printUsage()
    sys.exit(2)

  for opt, arg in opts:
    if opt in ('-h', '--help'):
      _printUsage()
      sys.exit()
    elif opt in ('--host'):
      host = arg
    elif opt in ('--port'):
      try:
        port = int(arg)
      except ValueError:
        pass
    elif opt in ('--log='):
      loglevel = arg

  _initializeLogging(loglevel)
  logger.debug("Main started")

  # Setup mqtt client
  client = MqttClient(host, port, clientId)
  client.startAsync()
  time.sleep(2)

  client.publish("roboraptorz/notification/busy","")
  client.publish("roboraptorz/notification/crossingReached","")
  client.publish("roboraptorz/notification/busy","")
  client.publish("roboraptorz/notification/availableDirections","[[\"E\",\"B\"],[\"N\",\"B\"]]")
 # client.publish("roboraptorz/notification/availableDirections","Test")

  input("\n\nPress Enter to abort...\n\n")

  # Terminate
  client.stop()

  logger.debug("Terminate")

if __name__ == '__main__':
  main(sys.argv[1:])
