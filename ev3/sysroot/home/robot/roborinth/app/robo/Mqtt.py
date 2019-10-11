#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from time import sleep

class Mqtt:

	def __init__(self, mqttConfig, rootTopic):
		self.msgHandlers = dict()
		self.host = mqttConfig['host']
		self.port = mqttConfig['port']
		self.rootTopic = rootTopic + '/'

		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_disconnect = self.on_disconnect
		self.client.on_message = self.on_message

		self.intendedDisconnect = False
		self.isConnected = False
		self.statusChangedCallback = None
	
	def exec(self):
		self.intendedDisconnect = False
		keepConnected = True
		while keepConnected:
			if not self.isConnected and not self.intendedDisconnect:
				self.tryToConnect()
				self.client.loop_start()
			elif not self.isConnected and self.intendedDisconnect:
				print('exit mqtt')
				keepConnected = False
				break
			sleep(1)

	def tryToConnect(self):
		tryConnect = True
		tryCount = 0
		while tryConnect and not self.isConnected and not self.intendedDisconnect:
			tryCount = tryCount + 1
			if self.statusChangedCallback is not None:
				self.statusChangedCallback('Connecting (' + str(tryCount) + ')...')
			try:
				ret = self.client.connect(self.host, int(self.port), 60)
				print('connected return code: ' + str(ret))
				if ret == 0:
					tryConnect = False
					break
			except OSError as e:
				print(str(e))
			sleep(5)

	def on_connect(self, client, userdata, flags, rc):
		self.isConnected = True
		print('mqtt client connected with result code ' + str(rc))
		client.subscribe(self.rootTopic + 'test')
		for t in self.msgHandlers.keys():
			print(t)
			client.subscribe(t)
		if self.statusChangedCallback is not None:
			self.statusChangedCallback('Connected')

	def on_disconnect(self, client, userdata, rc):
		self.isConnected = False
		if not self.intendedDisconnect:
			print('unintended disconnect from host')
			if self.statusChangedCallback is not None:
				self.statusChangedCallback('Connection Lost')
		else:
			print('intended disconnect')
			if self.statusChangedCallback is not None:
				self.statusChangedCallback('Disconnected')

	def on_message(self, client, userdata, msg):
		payload = ''
		if type(msg.payload) is bytes:
			# payload has to be utf-8 encoded
			payload = msg.payload.decode('utf-8')
		else:
			print('payload type error. payload type is expected to be bytes')
			return
		
		if msg.topic not in self.msgHandlers:
			print('no message handler registered for message with payload: ' + payload)
		else:
			self.msgHandlers[msg.topic][1](msg.topic, self.msgHandlers[msg.topic][0], payload)

	def setStatusChangedCallback(self, callback):
		self.statusChangedCallback = callback

	def registerMessageHandler(self, requestTopic, responseTopic, messageHandler):
		rootRequestTopic = self.rootTopic + requestTopic

		if rootRequestTopic in self.msgHandlers.keys():
			print('messageHandler for this topic already registered')
			return
		self.msgHandlers[rootRequestTopic] = (responseTopic, messageHandler)

	def publish(self, topic, message):
		t = self.rootTopic + topic
		self.client.publish(t, message)

	def exit(self):
		self.intendedDisconnect = True
		self.client.disconnect()
