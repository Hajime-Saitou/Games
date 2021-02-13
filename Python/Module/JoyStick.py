# JoyStick
#
# Copyright (c) 2021 Hajime Saito
#
# Released under the MIT license.
# see https://opensource.org/licenses/MIT
import pygame
from pygame.locals import *
import Repeater

JOY_MAX_TRIGGER = 16

JOY_NOINPUT  = 0
JOY_UP       = 0x1 << JOY_MAX_TRIGGER
JOY_RIGHT    = 0x2 << JOY_MAX_TRIGGER
JOY_DOWN     = 0x4 << JOY_MAX_TRIGGER
JOY_LEFT     = 0x8 << JOY_MAX_TRIGGER

JOY_TRIGGER1  = 0x1 << 0
JOY_TRIGGER2  = 0x1 << 1
JOY_TRIGGER3  = 0x1 << 2
JOY_TRIGGER4  = 0x1 << 3
JOY_TRIGGER5  = 0x1 << 4
JOY_TRIGGER6  = 0x1 << 5
JOY_TRIGGER7  = 0x1 << 6
JOY_TRIGGER8  = 0x1 << 7
JOY_TRIGGER9  = 0x1 << 8
JOY_TRIGGER10 = 0x1 << 9
JOY_TRIGGER11 = 0x1 << 10
JOY_TRIGGER12 = 0x1 << 11
JOY_TRIGGER13 = 0x1 << 12
JOY_TRIGGER14 = 0x1 << 13
JOY_TRIGGER15 = 0x1 << 14
JOY_TRIGGER16 = 0x1 << 15

JOY_MASK_STICK = (JOY_UP | JOY_RIGHT | JOY_DOWN | JOY_LEFT)
JOY_MASK_BUTTON = ~JOY_MASK_STICK

class JoyStickBase(object):
	def __init__(self):
		self.data = JOY_NOINPUT
		self.prevData = JOY_NOINPUT
		self.xorData = JOY_NOINPUT
		self.latestButtonDown = JOY_NOINPUT
		self.latestButtonUp = JOY_NOINPUT

		self.repeater = Repeater.XorRepeater()
		self.repeater.setDefaultValue(JOY_NOINPUT)
		self.repeatedData = JOY_NOINPUT

	def update(self):
		# update self.data at subclass before call this.
		self.repeatedData = self.repeater.update(self.data)
		self.xorData = self.data ^ self.prevData
		self.latestButtonDown = self.xorData & self.data
		self.latestButtonUp = self.xorData & ~self.data
		self.prevData = self.data

class JoyKey(JoyStickBase):
	def __init__(self):
		super().__init__()
		self.vk_up = K_UP
		self.vk_right = K_RIGHT
		self.vk_down = K_DOWN
		self.vk_left = K_LEFT
		self.vk_button = [ 0 ] * JOY_MAX_TRIGGER
		self.vk_button[0] = K_z
		self.vk_button[1] = K_x
		self.vk_button[2] = K_c

	def update(self):
		key = pygame.key.get_pressed()

		self.data = JOY_NOINPUT
		if key[self.vk_up] == 1:
			self.data |= JOY_UP
		if key[self.vk_right] == 1:
			self.data |= JOY_RIGHT
		if key[self.vk_down] == 1:
			self.data |= JOY_DOWN
		if key[self.vk_left] == 1:
			self.data |= JOY_LEFT

		for i in range(JOY_MAX_TRIGGER):
			if key[self.vk_button[i]] == 1:
				self.data |= 1 << i

		super().update()

class JoyStick(JoyStickBase):
	def __init__(self, joyStickId=0):
		super().__init__()

		if joyStickId >= pygame.joystick.get_count():
			raise ValueError("Invalid JoyStick ID {}".format(joyStickId))

		self.joyStick = pygame.joystick.Joystick(joyStickId)
		self.joyStick.init()

		self.hasHat = True if self.joyStick.get_numhats() > 0 else False

	def update(self):
		self.data = JOY_NOINPUT

		stickDatas = []
		if self.hasHat:
			for i in range(self.joyStick.get_numhats()):
				x, y = self.joyStick.get_hat(i)
				stickDatas.extend([ x, -y ])
		else:
			for i in range(self.joyStick.get_numaxes()):
				stickDatas.append(self.joyStick.get_axis(i))

		if stickDatas[1] < -0.5:
			self.data |= JOY_UP
		if stickDatas[1] > 0.5:
			self.data |= JOY_DOWN

		if stickDatas[0] > 0.5:
			self.data |= JOY_RIGHT
		if stickDatas[0] < -0.5:
			self.data |= JOY_LEFT

		for i in range(self.joyStick.get_numbuttons()):
			if self.joyStick.get_button(i) == True:
				self.data |= 1 << i

		super().update()

class JoyStickIntegrator(JoyStickBase):
	def __init__(self):
		super().__init__()

		self.joySticks = []

	def append(self, joyStick):
		self.joySticks.append(joyStick)

	def remove(self, joyStick):
		self.joySticks.remove(joyStick)

	def update(self):
		self.data = JOY_NOINPUT
		self.repeatedData = JOY_NOINPUT
		self.xorData = JOY_NOINPUT
		self.latestButtonDown = JOY_NOINPUT
		self.latestButtonUp = JOY_NOINPUT

		for joyStick in self.joySticks:
			joyStick.update()
		
			self.data |= joyStick.data
			self.repeatedData |= joyStick.repeatedData
			self.xorData |= joyStick.xorData
			self.latestButtonDown |= joyStick.latestButtonDown
			self.latestButtonUp |= joyStick.latestButtonUp
