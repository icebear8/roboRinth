import logging

from .Common import *
from .Map import *

logger = logging.getLogger(__name__)

class MapMatcher:
    def __init__(self):
        self.globalMap = Map();
        self.roboMaps = {}
