#!/usr/bin/env python3

from ev3dev.auto import *
from robo.Ui import Ui
from robo.Mqtt import Mqtt
from robo.Io import Io
from robo.JsonConfig import loadJsonFile
import json

configFile = '../config/config.json'

def main():
	config = loadJsonFile(configFile)

	ui = Ui(config['robot'])
	mqtt = Mqtt(config['mqtt'], config['robot']['id'])
	io = Io()

	# Mqtt connection status
	def statusChangedCallback(status):
		ui.setStatusText(status)
		if status == 'Connected':
			ui.setStatusLed('green')
			# ui.playStartSound()
		else:
			ui.setStatusLed('orange')

	# Control Messages
	def handleControlMessage(topic, responseTopic, payload):
		if payload == 'Q':
			print('received Quit Command')
			mqtt.publish(responseTopic, str(True))
			mqtt.exit()
		else:
			mqtt.publish(responseTopic, str(False))

	def handleText(topic, responseTopic, payload):
		ui.setMessageText(payload)
		mqtt.publish(responseTopic, str(True))

	# TouchSensor
	def returnTouchSensorPresent(topic, responseTopic, payload):
		val = io.touchSensorPresent()
		mqtt.publish(responseTopic, str(val))

	def returnTouchSensorPressed(topic, responseTopic, payload):
		val = io.readTouchSensorPressed()
		mqtt.publish(responseTopic, str(val))

	# ColorSensor
	def returnColorSensorPresent(topic, responseTopic, payload):
		val = io.colorSensorPresent()
		mqtt.publish(responseTopic, str(val))

	def returnColorSensorReflectedLightIntensity(topic, responseTopic, payload):
		val = io.readReflectedLightIntensity()
		mqtt.publish(responseTopic, str(val))

	def returnColorSensorAmbientLightIntensity(topic, responseTopic, payload):
		val = io.readAmbientLightIntensity()
		mqtt.publish(responseTopic, str(val))

	def returnColorSensorColor(topic, responseTopic, payload):
		val = io.readColor()
		mqtt.publish(responseTopic, str(val))

	def returnColorSensorColorName(topic, responseTopic, payload):
		val = io.readColorName()
		mqtt.publish(responseTopic, str(val))

	def returnColorSensorColorRaw(topic, responseTopic, payload):
		val = io.readColorRaw()
		mqtt.publish(responseTopic, str(val))

	# UltrasonicSensor
	def returnUltrasonicSensorPresent(topic, responseTopic, payload):
		val = io.ultrasonicSensorPresent()
		mqtt.publish(responseTopic, str(val))

	def returnUltraSonicSensorDistanceCentimeter(topic, responseTopic, payload):
		val = io.readDistanceCentimeter()
		mqtt.publish(responseTopic, str(val))

	# GyroSensor
	def returnGyroSensorPresent(topic, responseTopic, payload):
		val = io.gyroSensorPresent()
		mqtt.publish(responseTopic, str(val))

	def resetGyroSensor(topic, responseTopic, payload):
		mqtt.publish(responseTopic, str(io.resetGyroSensor()))

	def returnGyroSensorAngle(topic, responseTopic, payload):
		val = io.readGyroAngle()
		mqtt.publish(responseTopic, str(val))

	# MediumMotor
	def returnMediumMotorPresent(topic, responseTopic, payload):
		val = io.mediumMotorPresent()
		mqtt.publish(responseTopic, str(val))

	def returnMediumMotorPosition(topic, responseTopic, payload):
		val = io.readMediumMotorPosition()
		mqtt.publish(responseTopic, str(val))

	def resetMediumMotorPosition(topic, responseTopic, payload):
		mqtt.publish(responseTopic, str(io.resetMediumMotorPosition()))

	def turnMediumMotorByAngle(topic, responseTopic, payload):
		data = json.loads(payload)
		angle = float(data['angle'])
		speed = float(data['speed'])
		mqtt.publish(responseTopic, str(io.turnMediumMotorByAngle(speed, angle)))

	def activateMediumMotor(topic, responseTopic, payload):
		val = float(payload)
		mqtt.publish(responseTopic, str(io.activateMediumMotor(val)))

	# MoveSteering
	def returnMoveSteeringPresent(topic, responseTopic, payload):
		val = io.moveSteeringPresent()
		mqtt.publish(responseTopic, str(val))

	def resetMoveSteering(topic, responseTopic, payload):
		mqtt.publish(responseTopic, str(io.resetMoveSteering()))

	def activateMoveSteering(topic, responseTopic, payload):
		data = json.loads(payload)
		steering = float(data['steering'])
		speed = float(data['speed'])
		mqtt.publish(responseTopic, str(io.activateMoveSteering(steering, speed)))

	def turnMoveSteeringByAngle(topic, responseTopic, payload):
		data = json.loads(payload)
		steering = float(data['steering'])
		speed = float(data['speed'])
		angle = float(data['angle'])
		mqtt.publish(responseTopic, str(io.turnMoveSteeringByAngle(speed, steering, angle)))

	def returnPowerVoltage(topic, responseTopic, payload):
		val = io.readVoltageV()
		mqtt.publish(responseTopic, str(val))

	def returnPowerCurrent(topic, responseTopic, payload):
		val = io.readCurrentMA()
		mqtt.publish(responseTopic, str(val))

	def setNotificationPeriod(topic, responseTopic, payload):
		val = float(payload)
		mqtt.publish(responseTopic, str(io.setNotificationPeriod(val)))

	# UI
	def handleBackspacePressed(isPressed):
		if isPressed:
			print('backspace pressed')
			print('disconnect')
			mqtt.exit()

	ui.registerBackspaceHandler(handleBackspacePressed)

	mqtt.setStatusChangedCallback(statusChangedCallback)

	mqtt.registerMessageHandler('request/ctrl', 'response/ctrl',  handleControlMessage)
	mqtt.registerMessageHandler('request/txt', 'response/txt', handleText)
	mqtt.registerMessageHandler('request/color/present', 'response/color/present', returnColorSensorPresent)
	mqtt.registerMessageHandler('request/color/reflected', 'response/color/reflected', returnColorSensorReflectedLightIntensity)
	mqtt.registerMessageHandler('request/color/ambient', 'response/color/ambient', returnColorSensorAmbientLightIntensity)
	mqtt.registerMessageHandler('request/color/id', 'response/color/id', returnColorSensorColor)
	mqtt.registerMessageHandler('request/color/name', 'response/color/name', returnColorSensorColorName)
	mqtt.registerMessageHandler('request/color/raw', 'response/color/raw', returnColorSensorColorRaw)
	mqtt.registerMessageHandler('request/touch/present', 'response/touch/present', returnTouchSensorPresent)
	mqtt.registerMessageHandler('request/touch/pressed', 'response/touch/pressed', returnTouchSensorPressed)
	mqtt.registerMessageHandler('request/ultrasonic/present', 'response/ultrasonic/present', returnUltrasonicSensorPresent)
	mqtt.registerMessageHandler('request/ultrasonic/distance', 'response/ultrasonic/distance', returnUltraSonicSensorDistanceCentimeter)
	mqtt.registerMessageHandler('request/gyro/present', 'response/gyro/present', returnGyroSensorPresent)
	mqtt.registerMessageHandler('request/gyro/angle', 'response/gyro/angle', returnGyroSensorAngle)
	mqtt.registerMessageHandler('request/gyro/reset', 'response/gyro/reset', resetGyroSensor)
	mqtt.registerMessageHandler('request/motor/present', 'response/motor/present', returnMediumMotorPresent)
	mqtt.registerMessageHandler('request/motor/position', 'response/motor/position', returnMediumMotorPosition)
	mqtt.registerMessageHandler('request/motor/reset', 'response/motor/reset', resetMediumMotorPosition)
	mqtt.registerMessageHandler('request/motor/turn', 'response/motor/turn', turnMediumMotorByAngle)
	mqtt.registerMessageHandler('request/motor/activate', 'response/motor/activate', activateMediumMotor)
	mqtt.registerMessageHandler('request/steering/present', 'response/steering/present', returnMoveSteeringPresent)
	mqtt.registerMessageHandler('request/steering/activate', 'response/steering/activate', activateMoveSteering)
	mqtt.registerMessageHandler('request/steering/reset', 'response/steering/reset', resetMoveSteering)
	mqtt.registerMessageHandler('request/steering/turn', 'response/steering/turn', turnMoveSteeringByAngle)
	mqtt.registerMessageHandler('request/power/voltage', 'response/power/voltage', returnPowerVoltage)
	mqtt.registerMessageHandler('request/power/current', 'response/power/current', returnPowerCurrent)
	mqtt.registerMessageHandler('request/notper', 'response/notper', setNotificationPeriod)

	mqtt.registerMessageHandler('subscribe/color/present', 'color-present', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/color/reflected', 'color-reflected', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/color/ambient', 'color-ambient', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/color/id', 'color-id', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/color/name', 'color-name', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/color/raw', 'color-raw', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/touch/present', 'touch-present', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/touch/pressed', 'touch-pressed', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/ultrasonic/present', 'ultrasonic-present', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/ultrasonic/distance', 'ultrasonic-distance', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/gyro/present', 'gyro-present', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/gyro/angle', 'gyro-angle', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/motor/present', 'motor-present', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/motor/position', 'motor-position', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/steering/present', 'steering-present', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/power/voltage', 'voltage', io.enableNotification)
	mqtt.registerMessageHandler('subscribe/power/current', 'current', io.enableNotification)

	mqtt.registerMessageHandler('unsubscribe/color/present', 'color-present', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/color/reflected', 'color-reflected', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/color/ambient', 'color-ambient', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/color/id', 'color-id', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/color/name', 'color-name', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/color/raw', 'color-raw', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/touch/present', 'touch-present', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/touch/pressed', 'touch-pressed', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/ultrasonic/present', 'ultrasonic-present', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/ultrasonic/distance', 'ultrasonic-distance', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/gyro/present', 'gyro-present', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/gyro/angle', 'gyro-angle', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/motor/present', 'motor-present', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/motor/position', 'motor-position', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/steering/present', 'steering-present', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/power/voltage', 'voltage', io.disableNotification)
	mqtt.registerMessageHandler('unsubscribe/power/current', 'current', io.disableNotification)

	io.registerNotificationCallback('color-present', 'notification/color/present', mqtt.publish)
	io.registerNotificationCallback('color-reflected', 'notification/color/reflected', mqtt.publish)
	io.registerNotificationCallback('color-ambient', 'notification/color/ambient', mqtt.publish)
	io.registerNotificationCallback('color-id', 'notification/color/id', mqtt.publish)
	io.registerNotificationCallback('color-name', 'notification/color/name', mqtt.publish)
	io.registerNotificationCallback('color-raw', 'notification/color/raw', mqtt.publish)
	io.registerNotificationCallback('touch-present', 'notification/touch/present', mqtt.publish)
	io.registerNotificationCallback('touch-pressed', 'notification/touch/pressed', mqtt.publish)
	io.registerNotificationCallback('ultrasonic-present', 'notification/ultrasonic/present', mqtt.publish)
	io.registerNotificationCallback('ultrasonic-distance', 'notification/ultrasonic/distance', mqtt.publish)
	io.registerNotificationCallback('gyro-present', 'notification/gyro/present', mqtt.publish)
	io.registerNotificationCallback('gyro-angle', 'notification/gyro/angle', mqtt.publish)
	io.registerNotificationCallback('motor-present', 'notification/motor/present', mqtt.publish)
	io.registerNotificationCallback('motor-position', 'notification/motor/position', mqtt.publish)
	io.registerNotificationCallback('steering-present', 'notification/steering/present', mqtt.publish)
	io.registerNotificationCallback('voltage', 'notification/power/voltage', mqtt.publish)
	io.registerNotificationCallback('current', 'notification/power/current', mqtt.publish)

	print('start io thread')
	io.start()
	print('start ui thread')
	ui.start()
	print('start mqtt client')
	mqtt.exec()  # blocking
	io.stop()
	ui.stop()
	print('quit application')

main()
