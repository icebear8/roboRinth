#!/usr/bin/env python3

from classes.JsonConfig import loadJsonFile

configFile = '../config/config.json'

def main():
	config = loadJsonFile(configFile)
	print(config['io']['MoveSteering'][0])
	print(config['io']['MoveSteering'][1])

main()