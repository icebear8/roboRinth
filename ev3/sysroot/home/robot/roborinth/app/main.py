#!/usr/bin/env python3

from ev3dev.auto import *
from classes.SimpleUi import SimpleUi
from classes.SimpleMqtt import SimpleMqtt
from classes.SimpleIO import SimpleIO
from classes.JsonConfig import loadJsonFile
import json

configFile = '../config/config.json'


def main():
	config = loadJsonFile(configFile)

	ui = SimpleUi(config['robot'])
	mqtt = SimpleMqtt(config['mqtt'], config['robot']['id'])
	io = SimpleIO(config['io'])

	
	# SimpleMqtt

	def statusChangedCallback(status):
		ui.setStatusText(status)
		if status == 'Connected':
			ui.setStatusLed('green')
			ui.playStartSound()
		else:
			ui.setStatusLed('orange')


	# General Messages

	def handleControlMessage(topic, payload):
		print('handle control message: ' + payload)
		if payload == 'Q':
			print('disconnect')
			mqtt.disconnect()

	def handleText(topic, payload):
		print('handle text: ' + payload)
		ui.setMessageText(payload)


	# TouchSensor

	def returnTouchSensorPresent(topic, payload):
		val = io.touchSensorPresent()
		print('publish response TouchSensor present: ' + str(val))
		mqtt.publishResponse(topic, str(val))

	def returnTouchSensorPressed(topic, payload):
		val = io.readTouchSensorPressed()
		print('publish response TouchSensor pressed: ' + str(val))
		mqtt.publishResponse(topic, str(val))


	# ColorSensor

	def returnColorSensorPresent(topic, payload):
		val = io.colorSensorPresent()
		print('publish response ColorSensor present: ' + str(val))
		mqtt.publishResponse(topic, str(val))

	def returnColorSensorReflectedLightIntensity(topic, payload):
		val = io.readReflectedLightIntensity()
		print('publish response ColorSensor reflected light intensity: ' + str(val))
		mqtt.publishResponse(topic, str(val))

	def returnColorSensorAmbientLightIntensity(topic, payload):
		val = io.readAmbientLightIntensity()
		print('publish response ColorSensor ambient light intensity: ' + str(val))
		mqtt.publishResponse(topic, str(val))

	def returnColorSensorColor(topic, payload):
		val = io.readColor()
		print('publish response ColorSensor color: ' + str(val))
		mqtt.publishResponse(topic, str(val))

	def returnColorSensorColorName(topic, payload):
		val = io.readColorName()
		print('publish response ColorSensor color name: ' + str(val))
		mqtt.publishResponse(topic, str(val))

	def returnColorSensorColorRaw(topic, payload):
		val = io.readColorRaw()
		print('publish response ColorSensor color: ' + str(val))
		mqtt.publishResponse(topic, str(val))


	# UltrasonicSensor

	def returnUltrasonicSensorPresent(topic, payload):
		val = io.ultrasonicSensorPresent()
		print('publish response UltrasonicSensor present: ' + str(val))
		mqtt.publishResponse(topic, str(val))
	
	def returnUltraSonicSensorDistanceCentimeter(topic, payload):
		val = io.readDistanceCentimeter()
		print('publish response UltrasonicSensor distance centimeter: ' + str(val))
		mqtt.publishResponse(topic, str(val))


	# GyroSensor

	def returnGyroSensorPresent(topic, payload):
		val = io.gyroSensorPresent()
		print('publish response GyroSensor present: ' + str(val))
		mqtt.publishResponse(topic, str(val))
	
	def resetGyroSensor(topic, payload):
		print('reset GyroSensor')
		io.resetGyroSensor()
		
	def returnGyroSensorAngle(topic, payload):
		val = io.readGyroAngle()
		print('publish response GyroSensor angle: ' + str(val))
		mqtt.publishResponse(topic, str(val))


	# MediumMotor

	def returnMediumMotorPresent(topic, payload):
		val = io.mediumMotorPresent()
		print('publish response MediumMotor present: ' + str(val))
		mqtt.publishResponse(topic, str(val))

	def returnMediumMotorPosition(topic, payload):
		val = io.readMediumMotorPosition()
		print('publish response MediumMotor position: ' + str(val))
		mqtt.publishResponse(topic, str(val))

	def resetMediumMotorPosition(topic, payload):
		print('reset MediumMotor position')
		io.resetMediumMotorPosition()

	def turnMediumMotorByAngle(topic, payload):
		val = float(payload)
		print('turn MediumMotor by angle: ' + str(val))
		io.turnMediumMotorByAngle(val)

	def activateMediumMotor(topic, payload):
		val = float(payload)
		print('activate MediumMotor with duty cycle: ' + str(val))
		io.activateMediumMotor(val)
	

	# MoveSteering

	def returnMoveSteeringPresent(topic, payload):
		val = io.moveSteeringPresent()
		print('publish response MoveSteering present: ' + str(val))
		mqtt.publishResponse(topic, str(val))

	def resetMoveSteering(topic, payload):
		print('reset MoveSteering')
		io.resetMoveSteering()

	def activateMoveSteering(topic, payload):
		data = json.loads(payload)
		steering = float(data['steering'])
		speed = float(data['speed'])
		print('activate MediumMotor with steering: ' + str(steering) + ' and speed: ' + str(speed))
		io.activateMoveSteering(steering, speed)

	def turnMoveSteeringByAngle(topic, payload):
		val = float(payload)
		print('turn MoveSteering by angle: ' + str(val))
		io.turnMoveSteeringByAngle(val)

	# UI

	def handleBackspacePressed(isPressed):
		if isPressed:
			print('backspace pressed')
			print('disconnect')
			mqtt.exit()


	ui.registerBackspaceHandler(handleBackspacePressed)
	ui.start()
	ui.setPowerSupplyText(str(round(io.readVoltageUV()/1000000,1)) + ' V / ' + str(int(round(io.readCurrentUA()/1000,0))) + ' mA') 

	mqtt.setStatusChangedCallback(statusChangedCallback)
	mqtt.registerMessageHandler('ctrl', handleControlMessage)
	mqtt.registerMessageHandler('txt', handleText)
	mqtt.registerMessageHandler('color/present', returnColorSensorPresent)
	mqtt.registerMessageHandler('color/reflected', returnColorSensorReflectedLightIntensity)
	mqtt.registerMessageHandler('color/ambient', returnColorSensorAmbientLightIntensity)
	mqtt.registerMessageHandler('color/color', returnColorSensorColor)
	mqtt.registerMessageHandler('color/colorname', returnColorSensorColorName)
	mqtt.registerMessageHandler('color/colorraw', returnColorSensorColorRaw)
	mqtt.registerMessageHandler('touch/present', returnTouchSensorPresent)
	mqtt.registerMessageHandler('touch/pressed', returnTouchSensorPressed)
	mqtt.registerMessageHandler('ultrasonic/present', returnUltrasonicSensorPresent)
	mqtt.registerMessageHandler('ultrasonic/distance', returnUltraSonicSensorDistanceCentimeter)
	mqtt.registerMessageHandler('gyro/present', returnGyroSensorPresent)
	mqtt.registerMessageHandler('gyro/angle', returnGyroSensorAngle)
	mqtt.registerMessageHandler('gyro/reset', resetGyroSensor)
	mqtt.registerMessageHandler('motor/present', returnMediumMotorPresent)
	mqtt.registerMessageHandler('motor/position', returnMediumMotorPosition)
	mqtt.registerMessageHandler('motor/reset', resetMediumMotorPosition)
	mqtt.registerMessageHandler('motor/turn', turnMediumMotorByAngle)
	mqtt.registerMessageHandler('motor/activate', activateMediumMotor)
	mqtt.registerMessageHandler('steering/present', returnMoveSteeringPresent)
	mqtt.registerMessageHandler('steering/activate', activateMoveSteering)
	mqtt.registerMessageHandler('steering/reset', resetMoveSteering)
	mqtt.registerMessageHandler('steering/turn', turnMoveSteeringByAngle)

	
	mqtt.exec()
	ui.stop()
	print('quit application')

main()
