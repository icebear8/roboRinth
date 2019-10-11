#!/usr/bin/env python3

import threading
from time import sleep

from ev3dev2.display import Display
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.led import Leds

import ev3dev2.fonts as fonts


class Ui(threading.Thread):
	M_FONT = 'helvB12'

	def __init__(self, config):
		threading.Thread.__init__(self)
		self.roboId = config['id']
		self.threadID = 1
		self.name = 'ui-thread'
		self.isRunning = True
		self.messageText = '-'
		self.statusText = '-'
		self.powerSupplyText = '-'
		self.lcd = Display()
		self.btn = Button()
		self.sound = Sound()
		self.leds = Leds()
		self.theFont = fonts.load(Ui.M_FONT)
		self.lcd.clear()
		self.drawText()
		self.lcd.update()

	def drawText(self):
		self.lcd.draw.text((0, 0), 'RoboRinth', font=self.theFont)
		self.lcd.draw.text((0, 14), 'ID: ' + self.roboId, font=self.theFont)
		self.lcd.draw.text((0, 28), 'Status: ' + self.statusText, font=self.theFont)
		self.lcd.draw.text((0, 42), 'Msg: ' + self.messageText, font=self.theFont)
		# self.lcd.draw.text((0,56), 'Pwr: ' + self.powerSupplyText, font=self.theFont)

	def run(self):
		while self.isRunning:
			self.lcd.clear()
			self.drawText()
			self.lcd.update()
			self.btn.process()
			sleep(1)
		# sleep(0.5)
		self.lcd.clear()
		self.lcd.draw.rectangle((0, 0, 178, 128), fill='white')
		self.lcd.update()

	def registerBackspaceHandler(self, backspaceHandler):
		self.btn.on_backspace = backspaceHandler

	def stop(self):
		self.isRunning = False
		self.join()

	def setMessageText(self, text):
		self.messageText = text

	def setStatusText(self, text):
		self.statusText = text

	def setPowerSupplyText(self, text):
		self.powerSupplyText = text;

	def playStartSound(self):
		self.sound.tone([(800, 200, 0), (1200, 400, 100)])

	def setStatusLed(self, color):
		if color == 'green':
			self.leds.set_color('RIGHT', 'GREEN')
		elif color == 'orange':
			self.leds.set_color('RIGHT', 'ORANGE')
		else:
			print('unsupported color: ' + str(color))
