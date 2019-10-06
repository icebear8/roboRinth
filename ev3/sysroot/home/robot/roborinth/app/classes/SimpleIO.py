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

	def __init__(self):
		threading.Thread.__init__(self)
		self.threadID = 1
		self.name = 'io-thread'
		self.isRunning = True
		try:
			touchSensorInputs = self.findTouchSensors()
			if len(touchSensorInputs) == 0:
				raise DeviceNotFound('No TouchSensors found')
			self.touchSensor = TouchSensor(touchSensorInputs[0])
		except DeviceNotFound as err:
			self.touchSensor = None
			print(str(err)) 

		try:
			colorSensorInputs = self.findColorSensors()
			if len(colorSensorInputs) == 0:
				raise DeviceNotFound('No ColorSensors found')
			self.colorSensor = ColorSensor(colorSensorInputs[0])
		except DeviceNotFound as err:
			self.colorSensor = None
			print(str(err)) 

		try:
			ultrasonicSensorInputs = self.findUltrasonicSensors()
			if len(ultrasonicSensorInputs) == 0:
				raise DeviceNotFound('No UltrasonicSensors found')
			self.ultrasonicSensor = UltrasonicSensor(ultrasonicSensorInputs[0])
		except DeviceNotFound as err:
			self.ultrasonicSensor = None
			print(str(err)) 

		try:
			gyroSensorInputs = self.findGyroSensors()
			if len(gyroSensorInputs) == 0:
				raise DeviceNotFound('No GyroSensors found')
			self.gyroSensor = GyroSensor(gyroSensorInputs[0])
		except DeviceNotFound as err:
			self.gyroSensor = None
			print(str(err)) 

		try:
			mediumMotorInputs = self.findMediumMotors()
			if len(mediumMotorInputs) == 0:
				raise DeviceNotFound('No MediumMotors found')
			self.mediumMotor = MediumMotor(mediumMotorInputs[0])
		except DeviceNotFound as err:
			self.mediumMotor = None
			print(str(err)) 

		try:
			largeMotorInputs = self.findLargeMotors()
			if len(largeMotorInputs) < 2:
				raise DeviceNotFound('Too few LargeMotors found')
			self.moveSteering = MoveSteering(largeMotorInputs[0], largeMotorInputs[1])
		except DeviceNotFound as err:
			self.moveSteering = None
			print(str(err)) 

		self.powerSupply = PowerSupply()

		self.readAll()
		self.resetMediumMotorPosition()
		self.resetMoveSteering()
		self.resetGyroSensor()
		sleep(3) # make sure reset calls from before have an effect
		self.readAll()
		

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
		except (OSError, ValueError, AttributeError, DeviceNotFound) as e:
			self.colorSensor = None
		return 0

	def readAmbientLightIntensity(self):
		try:
			return self.colorSensor.ambient_light_intensity
		except (OSError, ValueError, AttributeError, DeviceNotFound) as e:
			self.colorSensor = None
		return 0		

	def readColor(self):
		try:
			return self.colorSensor.color
		except (OSError, AttributeError, DeviceNotFound) as e:
			self.colorSensor = None
		return 0

	def readColorName(self):
		try:
			return self.colorSensor.color_name
		except (OSError, AttributeError, DeviceNotFound) as e:
			self.colorSensor = None
		return 'NoColor'

	def readColorRaw(self):
		try:
			return self.colorSensor.raw
		except (OSError, AttributeError, DeviceNotFound) as e:
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
			#self.gyroSensor.reset()
			self.gyroSensor._direct = self.gyroSensor.set_attr_raw(self.gyroSensor._direct, 'direct', bytes(17,))
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
			self.mediumMotor.on(0, brake=False)
			self.mediumMotor.position = 0
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

	def readCurrentMA(self):
		return round(self.powerSupply.measured_current / 1000, 1)

	def readVoltageV(self):
		return round(self.powerSupply.measured_voltage / 1000000, 1)

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
			str(self.readMediumMotorPosition()) + '\t' +
			str(self.readCurrentMA()) + '\t' +
			str(self.readVoltageV())
		)

	def run(self):
		while self.isRunning:
			# todo read sensors and call notify callbacks on change
			sleep(0.1)

	def stop(self):
		self.isRunning = False
		self.join()
