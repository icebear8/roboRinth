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


class Io(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.threadID = 1
		self.name = 'io-thread'
		self.isRunning = True
		self.notificationCallbacks = dict()
		self.period = 1

		'''try:
			touchSensorInputs = self.findTouchSensors()
			if len(touchSensorInputs) == 0:
				raise DeviceNotFound('No TouchSensors found')
			self.touchSensor = TouchSensor(touchSensorInputs[0])
		except DeviceNotFound as err:'''
		self.touchSensor = None
		# print(str(err))

		try:
			colorSensorInputs = self.findColorSensors()
			if len(colorSensorInputs) == 0:
				raise DeviceNotFound('No ColorSensors found')
			self.colorSensor = ColorSensor(colorSensorInputs[0])
		except DeviceNotFound as err:
			self.colorSensor = None
			print(str(err))

		'''try:
			ultrasonicSensorInputs = self.findUltrasonicSensors()
			if len(ultrasonicSensorInputs) == 0:
				raise DeviceNotFound('No UltrasonicSensors found')
			self.ultrasonicSensor = UltrasonicSensor(ultrasonicSensorInputs[0])
		except DeviceNotFound as err:'''
		self.ultrasonicSensor = None
		# print(str(err))

		try:
			gyroSensorInputs = self.findGyroSensors()
			if len(gyroSensorInputs) == 0:
				raise DeviceNotFound('No GyroSensors found')
			self.gyroSensor = GyroSensor(gyroSensorInputs[0])
		except DeviceNotFound as err:
			self.gyroSensor = None
			print(str(err))


		'''try:
			mediumMotorInputs = self.findMediumMotors()
			if len(mediumMotorInputs) == 0:
				raise DeviceNotFound('No MediumMotors found')
			self.mediumMotor = MediumMotor(mediumMotorInputs[0])
		except DeviceNotFound as err:'''
		self.mediumMotor = None
		# print(str(err))

		try:
			largeMotorInputs = self.findLargeMotors()
			if len(largeMotorInputs) < 2:
				raise DeviceNotFound('Too few LargeMotors found')
			self.moveSteering = MoveSteering(largeMotorInputs[0], largeMotorInputs[1])
		except DeviceNotFound as err:
			self.moveSteering = None
			print(str(err))

		self.powerSupply = PowerSupply()

		# observed many times application freezes when executing the following lines
		# introduced sleeps as workaround. hopefully this gives the drivers enough time to reset and prevent freeze
		print('reset sensors...')
		sleep(3)
		# self.resetMediumMotorPosition()
		self.resetMoveSteering()
		sleep(1)
		self.resetGyroSensor()
		sleep(3)
		print('Done.')

	def findDevices(self, driverName, ioNames, list_method):
		findings = []
		for io in ioNames:
			result = list_method('*', driver_name=driverName, address=io)
			found = bool(sum(1 for r in result))
			if found:
				findings.append(io)
				print('found device with driver name ' + driverName + ' on io ' + io)
		return findings

	def findSensors(self, driverName):
		ios = ['in1', 'in2', 'in3', 'in4']
		return self.findDevices(driverName, ios, list_sensors)

	def findTouchSensors(self):
		driverName = 'lego-ev3-touch'
		return self.findSensors(driverName)

	def findColorSensors(self):
		driverName = 'lego-ev3-color'
		return self.findSensors(driverName)

	def findUltrasonicSensors(self):
		driverName = 'lego-ev3-us'
		return self.findSensors(driverName)

	def findGyroSensors(self):
		driverName = 'lego-ev3-gyro'
		return self.findSensors(driverName)

	def findMotors(self, driverName):
		ios = ['outA', 'outB', 'outC', 'outD']
		return self.findDevices(driverName, ios, list_motors)

	def findMediumMotors(self):
		driverName = 'lego-ev3-m-motor'
		return self.findMotors(driverName)

	def findLargeMotors(self):
		driverName = 'lego-ev3-l-motor'
		return self.findMotors(driverName)

	# TouchSensor

	def touchSensorPresent(self):
		return self.touchSensor is not None

	def readTouchSensorPressed(self):
		try:
			return self.touchSensor.is_pressed == 1
		except (OSError, AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable TouchSensor!')
			self.touchSensor = None
		except ValueError as e:
			print(str(e))
		return False

	# ColorSensor

	def colorSensorPresent(self):
		return self.colorSensor is not None

	def readReflectedLightIntensity(self):
		try:
			return self.colorSensor.reflected_light_intensity
		except (OSError, AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable  ColorSensor!')
			self.colorSensor = None
		except ValueError as e:
			print(str(e))
		return 0

	def readAmbientLightIntensity(self):
		try:
			return self.colorSensor.ambient_light_intensity
		except (OSError, AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable ColorSensor')
			self.colorSensor = None
		except ValueError as e:
			print(str(e))
		return 0

	def readColor(self):
		try:
			return self.colorSensor.color
		except (OSError, AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable ColorSensor')
			self.colorSensor = None
		except ValueError as e:
			print(str(e))
		return 0

	def readColorName(self):
		try:
			return self.colorSensor.color_name
		except (OSError, AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable ColorSensor')
			self.colorSensor = None
		except ValueError as e:
			print(str(e))
		return 'NoColor'

	def readColorRaw(self):
		try:
			return self.colorSensor.raw
		except (OSError, AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable  ColorSensor')
			self.colorSensor = None
		except ValueError as e:
			print(str(e))
		return 0, 0, 0

	# UltrasonicSensor

	def ultrasonicSensorPresent(self):
		return self.ultrasonicSensor is not None

	def readDistanceCentimeter(self):
		try:
			return round(self.ultrasonicSensor.distance_centimeters_continuous, 1)
		except (AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable UltrasonicSensor')
			self.ultrasonicSensor = None
		except ValueError as e:
			print(str(e))
		return 0.0

	# GyroSensor

	def gyroSensorPresent(self):
		return self.gyroSensor is not None

	def resetGyroSensor(self):
		try:
			# self.gyroSensor.reset() --> this official api method does not works
			self.gyroSensor._direct = self.gyroSensor.set_attr_raw(self.gyroSensor._direct, 'direct', bytes(17, ))
			return True
		except (OSError, AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable GyroSensor')
			self.gyroSensor = None
		except ValueError as e:
			print(str(e))
		return False

	def readGyroAngle(self):
		try:
			return self.gyroSensor.angle
		except (OSError, AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable GyroSensor')
			self.gyroSensor = None
		except ValueError as e:
			print(str(e))
		return 0

	# MediumMotor

	def mediumMotorPresent(self):
		return self.mediumMotor is not None

	def readMediumMotorPosition(self):
		try:
			return self.mediumMotor.position
		except (AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable MediumMotor')
			self.mediumMotor = None
		except ValueError as e:
			print(str(e))
		return 0

	def resetMediumMotorPosition(self):
		try:
			self.mediumMotor.on(0, brake=False)
			self.mediumMotor.position = 0
			return True
		except (AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable MediumMotor')
			self.mediumMotor = None
		except ValueError as e:
			print(str(e))
		return False

	def turnMediumMotorByAngle(self, speed, angle):
		try:
			self.mediumMotor.on_for_degrees(speed, angle)
			return True
		except(AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable MediumMotor')
			self.mediumMotor = None
		except ValueError as e:
			print(str(e))
		return False

	def activateMediumMotor(self, dutyCycle):
		try:
			self.mediumMotor.on(dutyCycle)
			return True
		except(AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable MediumMotor')
			self.mediumMotor = None
		except ValueError as e:
			print(str(e))
		return False

	# MoveSteering

	def moveSteeringPresent(self):
		return self.moveSteering is not None

	def resetMoveSteering(self):
		try:
			self.moveSteering.on(0, 0)
			return True
		except (AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable MoveSteering')
			self.moveSteering = None
		except ValueError as e:
			print(str(e))
		return False

	def activateMoveSteering(self, steering, speed):
		try:
			self.moveSteering.on(steering, speed)
			return True
		except(AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable MoveSteering')
			self.moveSteering = None
		except ValueError as e:
			print(str(e))
		return False

	def turnMoveSteeringByAngle(self, speed, steering, angle):
		try:
			self.moveSteering.on_for_degrees(steering, speed, angle)
			return True
		except(AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable MoveSteering')
			self.moveSteering = None
		except ValueError as e:
			print(str(e))
		return False

	# PowerSupply

	def readCurrentMA(self):
		try:
			return round(self.powerSupply.measured_current / 1000, 1)
		except(AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable PowerSupply (ev3Driver)')
			self.powerSupply = None
		except ValueError as e:
			print(str(e))
		return 0

	def readVoltageV(self):
		try:
			return round(self.powerSupply.measured_voltage / 1000000, 1)
		except(AttributeError, DeviceNotFound) as e:
			print(str(e))
			print('Disable PowerSupply (ev3Driver)')
			self.powerSupply = None
		except ValueError as e:
			print(str(e))
		return 0

	def enableNotification(self, topic, notificationId, data):

		if notificationId in self.notificationCallbacks.keys():
			print('enable notification for id: ' + notificationId)
			self.notificationCallbacks[notificationId][0] = True
		else:
			print('cannot enable notification. no notification callback registered under id: ' + notificationId)

	def disableNotification(self, topic, notificationId, data):
		if notificationId in self.notificationCallbacks.keys():
			print('disable notification for id: ' + notificationId)
			self.notificationCallbacks[notificationId][0] = False
		else:
			print('cannot disable notification. no notification callback registered under id: ' + notificationId)

	def registerNotificationCallback(self, notificationId, data, callback):
		if notificationId in self.notificationCallbacks.keys():
			print('notification callback for this device already registered')
		else:
			readFunc = self.getReadFunc(notificationId)
			self.notificationCallbacks[notificationId] = [False, callback, data, readFunc]

	def getReadFunc(self, notificationId):
		if notificationId == 'color-present':
			return self.colorSensorPresent
		elif notificationId == 'color-reflected':
			return self.readReflectedLightIntensity
		elif notificationId == 'color-ambient':
			return self.readAmbientLightIntensity
		elif notificationId == 'color-id':
			return self.readColor
		elif notificationId == 'color-name':
			return self.readColorName
		elif notificationId == 'color-raw':
			return self.readColorRaw
		elif notificationId == 'touch-present':
			return self.touchSensorPresent
		elif notificationId == 'touch-pressed':
			return self.readTouchSensorPressed
		elif notificationId == 'ultrasonic-present':
			return self.ultrasonicSensorPresent
		elif notificationId == 'ultrasonic-distance':
			return self.readDistanceCentimeter
		elif notificationId == 'gyro-present':
			return self.gyroSensorPresent
		elif notificationId == 'gyro-angle':
			return self.readGyroAngle
		elif notificationId == 'motor-present':
			return self.mediumMotorPresent
		elif notificationId == 'motor-position':
			return self.readMediumMotorPosition
		elif notificationId == 'steering-present':
			return self.moveSteeringPresent
		elif notificationId == 'voltage':
			return self.readVoltageV
		elif notificationId == 'current':
			return self.readCurrentMA
		else:
			print('no read func for id: ' + notificationId)
			return None

	def notify(self, notificationId, value):
		if notificationId in self.notificationCallbacks.keys():
			self.notificationCallbacks[notificationId](value)

	def setNotificationPeriod(self, milliseconds):
		if 10 <= milliseconds <= 10000:
			self.period = milliseconds/1000
			return True
		return False

	def run(self):
		while self.isRunning:

			for id in self.notificationCallbacks.keys():
				enabled = self.notificationCallbacks[id][0]
				callback = self.notificationCallbacks[id][1]
				contextData = self.notificationCallbacks[id][2]
				readFunc = self.notificationCallbacks[id][3]
				if enabled:
					callback(contextData, str(readFunc()))
			sleep(self.period)

	def stop(self):
		self.isRunning = False
		self.join()
