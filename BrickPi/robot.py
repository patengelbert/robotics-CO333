from __future__ import print_function
import brickpi
import math
import time
from ConfigParser import RawConfigParser
from eventTypes import EventType, EventState
from motor import Motor
from sensor import PushSensor #, UltrasonicSensor

class Events:
	data = {}
	
	def add(name, event):
		if data.get(name) is None:
			data[name] = [event]
		else:
			data[name].add(event)

	def invoke(name, params):
		if data.get(name) is None:
			return
		for handler in data.get(name):
			handler(params)
	
class Robot:

	######################
	### Initialisation ###
	######################

	def initMotorParams(self, motorParams):
		motorParams.maxRotationAcceleration = 10
		motorParams.maxRotationSpeed = 20
		motorParams.feedForwardGain = 255/20
		motorParams.minPWM = 18
		motorParams.pidParameters.minOutput = -255
		motorParams.pidParameters.maxOutput = 255
	
	def initConfig(self):
		config = RawConfigParser()
		config.optionxform = str
		config.read('robot.cfg')
		for (item, value) in config.items('Robot'):
			setattr(self, item, float(value))
		print("Robot config loaded")
	
	def setDefaults(self):
		# Default config values
		self.deltaTime = 0.1
		self.powerL = 1
		self.powerR = 1
		self.rotatePower = 0.95

		self.movementCoeff = 36.363636
		self.botRadius = 0.08
		
		self.pidk_p = 600
		self.pidk_i = 100
		self.pidk_d = 20

	def __init__(self):
		self.setDefaults()
		self.interface = brickpi.Interface()
		self.interface.initialize()
		self.events = Events()
		self.motorL = Motor(self.interface, self.events, 0)
		self.motorR = Motor(self.interface, self.events, 1)
		self.initMotorParams(self.motorL.motorParams)
		self.initMotorParams(self.motorR.motorParams)

		self.initConfig()
		self.touchSensorL = PushSensor('left',  self.interface, 0, self.events, brickpi.SensorType.SENSOR_TOUCH)
		self.touchSensorR = PushSensor('right', self.interface, 1, self.events, brickpi.SensorType.SENSOR_TOUCH)
		self.setPID(self.pidk_p, self.pidk_i, self.pidk_d)

		self.events.add(EventType.SENSOR_TOUCH, sensorAction)
	
	###############
	### Logging ###
	###############

	def setLogging(self, log):
		self.logging = log

	def startLogging(self, optargs):
		if self.logging:
			optargs = [optarg for optarg in optargs if optarg is not None]
			optargs_str = '_'.join(str(optarg) for optarg in optargs)
			self.logName = './logs/' + \
				str(int(time.time())) +'_p' + \
				str(self.pidk_p) + '_i' + \
				str(self.pidk_i) + '_d' + \
				str(self.pidk_d) + '_' + optargs_str + '.log'
			self.interface.startLogging(self.logName)

	def stopLogging(self):
		if self.logging:
			self.interface.stopLogging()

	########################
	### 'with' statement ###
	########################

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.interface.terminate()

	#####################
	### Motor control ###
	#####################
	
	def setPID(self, p, i, d):
		self.motorL.setPID(p, i, d)
		self.motorR.setPID(p, i, d)
	
	def isMoving(self):
		return self.motorL.isRotating() or self.motorR.isRotating()

	def move(self, distance):
		# distance specified in metres
		wheel = distance * self.movementCoeff
		self.startLogging(['move', distance])
		self.motorL.rotate(self.powerL * wheel)
		self.motorR.rotate(self.powerR * wheel)
		self.stopLogging()
	
	def rotate(self, angle):
		# angle specified in degrees
		wheel = self.rotatePower * angle * (math.pi/180) * self.botRadius * self.movementCoeff
		self.startLogging(['turn', angle])
		self.motorL.rotate( self.powerL * wheel)
		self.motorR.rotate(-self.powerR * wheel)
		self.stopLogging()

	def arcPath(self, theta):
		# theta = 0 returns to straight path
		# Positive theta => too far to the right => turn left
		if theta <= 0 :
			self.powerL = 1 
			self.powerR = 1 + theta
		else: 		
			self.powerL = 1 - theta
			self.powerR = 1 
	
	def wait(self):
		while self.isMoving():
			time.sleep(self.deltaTime)

	######################
	### Sensor control ###
	######################

	def mainLoop(self):
		self.running = True
		while self.running:
			self.touchSensorL.check()
			self.touchSensorR.check()
			self.motorL.check()
			self.motorR.check()
			time.sleep(self.deltaTime)

	def sensorAction(self):
		self.wait()
		# function triggered by the event handler when the touchsensor values are changed.
		if (self.touchSensorL.getState() == EventState.SENSOR_TOUCH_DOWN) \
			and (self.touchSensorR.getState() == EventState.SENSOR_TOUCH_DOWN):
			self.move(-20)
			self.wait()
			self.rotate(self, 90)
		elif self.touchSensorL.getState() == EventState.SENSOR_TOUCH_DOWN:
			self.move(-10)
			self.wait()
			self.rotate(self, 45)
		elif self.touchSensorL.getState() == EventState.SENSOR_TOUCH_DOWN:
			self.move(-10)
			self.wait()
			self.rotate(self, -45)
		

			
