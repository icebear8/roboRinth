#!/usr/bin/env python3

from classes.SimpleMqtt import SimpleMqtt
from classes.JsonConfig import loadJsonFile

configFile = '../config/config.json'

def main():
	print("test mqtt")
	config = loadJsonFile(configFile)
	mqtt = SimpleMqtt(config['mqtt'], config['robot']['id'])

	def echoMessage(topic, payload):
		print('echo received message: ' + payload)
		mqtt.publish(topic, payload)

	def showStateAndExit(topic, payload):
		print('is sensor present?' + payload)
		mqtt.disconnect()

	def onMqttConnected():
		print('connected')
		mqtt.publish('color/present/', 'asd')

	mqtt.registerMessageHandler('test/request', 'test/response', echoMessage)
	mqtt.registerMessageHandler('color/present/response', showStateAndExit)
	mqtt.setOnConnectCallback(onMqttConnected)
	mqtt.exec()

main()
