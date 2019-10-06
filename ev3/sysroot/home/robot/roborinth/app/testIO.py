#!/usr/bin/env python3

from classes.SimpleIO import SimpleIO
from classes.JsonConfig import loadJsonFile
from time import sleep

configFile = '../config/config.json'

def main():
	print("test io")
	config = loadJsonFile(configFile)
	io = SimpleIO(config['io'])

	while True:
		io.readAll()
		sleep(1)

main()
