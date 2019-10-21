
class DirectionController:
    def __init__(self):
        self._name = 'direction controller'

    def discover(self, client, userdata, msg):
        print('discover')