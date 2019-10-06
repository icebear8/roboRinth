#!/usr/bin/env python3

import json

def loadJsonFile(filePath):
	with open(filePath, 'r') as jsonFile:
		jsonData = json.load(jsonFile)
	return jsonData