#!/usr/bin/env python3

import threading
from time import sleep

from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor

from ev3dev2.motor import MediumMotor
from ev3dev2.motor import MoveSteering

from ev3dev2.sensor import list_sensors
from ev3dev2.motor import list_motors

from ev3dev2.power import PowerSupply

from ev3dev2 import DeviceNotFound

class SimpleIO(threading.Thread):

	def __init__(self, config):
		threading.Thread.__init__(self)
		self.threadID = 1
		self.name = 'io-thread'
		self.isRunning = True
		try:
			self.touchSensor = TouchSensor(config['TouchSensor'])
		except DeviceNotFound as err:
			self.touchSensor = None
			print(str(err)) 

		try:
			self.colorSensor = ColorSensor(config['ColorSensor'])
		except DeviceNotFound as err:
			self.colorSensor = None
			print(str(err)) 

		try:
			self.ultrasonicSensor = UltrasonicSensor(config['UltrasonicSensor'])
		except DeviceNotFound as err:
			self.ultrasonicSensor = None
			print(str(err)) 

		try:
			self.gyroSensor = GyroSensor(config['GyroSensor'])
		except DeviceNotFound as err:
			self.gyroSensor = None
			print(str(err)) 

		try:
			self.mediumMotor = MediumMotor(config['MediumMotor'])
		except DeviceNotFound as err:
			self.mediumMotor = None
			print(str(err)) 

		try:
			self.moveSteering = MoveSteering(config['MoveSteering'][0], config['MoveSteering'][1])
		except DeviceNotFound as err:
			self.moveSteering = None
			print(str(err)) 

		self.powerSupply = PowerSupply()


	#TouchSensor

	def touchSensorPresent(self):
		return self.touchSensor is not None

	def readTouchSensorPressed(self):
		try:
			return (self.touchSensor.is_pressed == 1)
		except (AttributeError, DeviceNotFound) as e:
			self.touchSensor = None
		return False


	#ColorSensor

	def colorSensorPresent(self):
		return self.colorSensor is not None

	def readReflectedLightIntensity(self):
		try:
			return self.colorSensor.reflected_light_intensity
		except (ValueError, AttributeError, DeviceNotFound) as e:
			self.colorSensor = None
		return 0

	def readAmbientLightIntensity(self):
		try:
			return self.colorSensor.ambient_light_intensity
		except (AttributeError, DeviceNotFound) as e:
			self.colorSensor = None
		return 0		

	def readColor(self):
		try:
			return self.colorSensor.color
		except (AttributeError, DeviceNotFound) as e:
			self.colorSensor = None
		return 0

	def readColorName(self):
		try:
			return self.colorSensor.color_name
		except (AttributeError, DeviceNotFound) as e:
			self.colorSensor = None
		return 'NoColor'

	def readColorRaw(self):
		try:
			return self.colorSensor.raw
		except (AttributeError, DeviceNotFound) as e:
			self.colorSensor = None
		return 0, 0, 0


	#UltrasonicSensor

	def ultrasonicSensorPresent(self):
		return self.ultrasonicSensor is not None

	def readDistanceCentimeter(self):
		try:
			return round(self.ultrasonicSensor.distance_centimeters_continuous,1)
		except (AttributeError, DeviceNotFound) as e:
			self.ultrasonicSensor = None
		return 0.0


	#GyroSensor

	def gyroSensorPresent(self):
		return self.gyroSensor is not None

	def resetGyroSensor(self):
		try:
			self.gyroSensor.reset()
		except (AttributeError, DeviceNotFound) as e:
			self.gyroSensor = None

	def readGyroAngle(self):
		try:
			return self.gyroSensor.angle
		except (AttributeError, DeviceNotFound) as e:
			self.gyroSensor = None
		return 0


	#MediumMotor

	def mediumMotorPresent(self):
		return self.mediumMotor is not None

	def readMediumMotorPosition(self):
		try:
			return self.mediumMotor.position
		except (AttributeError, DeviceNotFound) as e:
			self.mediumMotor = None
		return 0

	def resetMediumMotorPosition(self):
		try:
			print('before, motor pos ' + str(self.mediumMotor.position)) 
			self.mediumMotor.on(0, brake=False)
			self.mediumMotor.position = 0
			print('after, motor pos ' + str(self.mediumMotor.position))
		except (AttributeError, DeviceNotFound) as e:
			self.mediumMotor = None

	def turnMediumMotorByAngle(self, angle):
		try:
			self.mediumMotor.on_for_degrees(80, angle)
		except(AttributeError, DeviceNotFound) as e:
			self.mediumMotor = None

	def activateMediumMotor(self, dutyCycle):
		try:
			self.mediumMotor.on(dutyCycle)
		except(AttributeError, DeviceNotFound) as e:
			self.mediumMotor = None



	#MoveSteering

	def moveSteeringPresent(self):
		return self.moveSteering is not None

	def resetMoveSteering(self):
		try:
			self.moveSteering.on(0, 0)
		except (AttributeError, DeviceNotFound) as e:
			self.moveSteering = None

	def activateMoveSteering(self, steering, speed):
		try:
			self.moveSteering.on(steering, speed)
		except(AttributeError, DeviceNotFound) as e:
			self.moveSteering = None

	def turnMoveSteeringByAngle(self, angle):
		try:
			self.moveSteering.on_for_degrees(100, 50, angle)
		except(AttributeError, DeviceNotFound) as e:
			self.moveSteering = None



	#PowerSupply

	def readCurrentUA(self):
		return self.powerSupply.measured_current

	def readVoltageUV(self):
		return self.powerSupply.measured_voltage

	#others

	def readAll(self):
		print(
			str(self.readTouchSensorPressed()) + '\t' +
			str(self.readAmbientLightIntensity()) + '\t' +
			str(self.readReflectedLightIntensity()) + '\t' +
	 		str(self.readColor()) + '\t' +
			str(self.readColorName()) + '\t' +
			str(self.readColorRaw()) + '\t' +
			str(self.readDistanceCentimeter()) + '\t' +
			str(self.readGyroAngle()) + '\t' +
			str(self.readMediumMotorPosition())
		)

	def run(self):
		while self.isRunning:
			# todo read sensors and call notify callbacks on change
			sleep(0.1)

	def stop(self):
		self.isRunning = False
		self.join()
