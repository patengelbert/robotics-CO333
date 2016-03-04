#import brickpi
from eventTypes import EventType, EventState
from ConfigParser import RawConfigParser
from motor import Motor

import math
import time

"""
Base class for sensors, enabling it on the given port
"""
class Sensor(object):
	
	def __init__(self, interface, port, events, sensorType):
		self.interface = interface
		self.port = port
		self.events = events
		self.sensorType = sensorType
		self.initConfig()
		interface.sensorEnable(port, self.sensorType)

	def check(self):
		raise NotImplementedError()

	def initConfig(self):
		config = RawConfigParser()
		config.optionxform = str
		config.read('robot.cfg')
		for (item, value) in config.items('Sensor'):
			setattr(self, item, float(value))
		for (item, value) in config.items('Debug'):
			setattr(self, item, bool(value))
		if self.debug:
			print "Sensor" + str(self.sensorType) + " Config loaded"

"""
A single touch sensor
"""
class PushSensor(Sensor):

	def __init__(self, position, *args, **kwargs):
		self.position = position
		super(PushSensor, self).__init__(*args, **kwargs)
		self.state = False

	def check(self):
		cvalue = bool(self.interface.getSensorValue(self.port)[0])
		if cvalue != self.state:
			self.state = cvalue
			self.events.invoke(EventType.SENSOR_TOUCH, {'position': self.position, 'down': cvalue})

	def getState(self):
		return self.state

"""
Single ultrasonic sensor
"""
class UltraSonicSensor(Sensor):
	def __init__(self, *args, **kwargs):
		self.ultrasonicOffset = -4
		self.ultrasonicInfValue = 255
		super(UltraSonicSensor, self).__init__(*args, **kwargs)
		self.value = 0
		self.ultrasonicScans = 20
		self.motor = Motor(self.interface, self.events, 3)
		# Zero the motor to the current position
		self.motor.zero = self.motor.getPosition()
		self.motor.initMotorParams()
		self.motor.setPID(400, 100, 0)
		self.scanData = []
		self.raw_value = 255

	def check(self):
		ivalue = self.getValue()
		
		if(self.value != ivalue):
			if ivalue is not self.ultrasonicInfValue:
				self.value = ivalue
				self.events.invoke(EventType.SENSOR_ULTRASOUND, {'distance':ivalue})
	
	def getValue(self):
		ivalue = self.interface.getSensorValue(self.port)[0]
		self.raw_value = ivalue
		if ivalue == () or ivalue == None or ivalue == self.ultrasonicInfValue:
			ivalue = float('inf')
		else:
			ivalue = (ivalue - self.ultrasonicOffset)/100.0
		return ivalue

	def scan(self):
		self.scanData = []
		self.motor.setPosition(math.pi)
		if self.debug:
			print 'Starting Scan'
		self.getValue()
		self.scanData.append(self.raw_value)
		for i in range(1, self.ultrasonicScans):
			if self.debug:
				t = time.clock()
			self.motor.setPosition(math.pi-(2*math.pi*i)/self.ultrasonicScans)
			if self.debug:
				#print 'Rotate finished after ' + str(time.clock() - t)
				pass
			self.getValue()
			self.scanData.append(self.raw_value)
		if self.debug:
			print 'Finished Scan'
		self.motor.setPosition(0)
		
"""
Implements the 'either' and 'both' positions for two touch sensors
"""
class Bumper:

	leftDown = False
	rightDown = False

	def bumperEvent(self, params):
		wasBoth = self.leftDown & self.rightDown
		wasEither = self.leftDown | self.rightDown
		if(params['position'] == 'left'):
			self.leftDown = params['down']
		if(params['position'] == 'right'):
			self.rightDown = params['down']
		isBoth = self.leftDown & self.rightDown
		isEither = self.leftDown | self.rightDown
		if(isBoth != wasBoth):
			self.events.invoke(EventType.SENSOR_TOUCH, {'position':'both', 'down':isBoth})
		if(isEither != wasEither):
			self.events.invoke(EventType.SENSOR_TOUCH, {'position':'either', 'down':isEither})

	def __init__(self, events):
		self.events = events
		events.add(EventType.SENSOR_TOUCH, self.bumperEvent)

