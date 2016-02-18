from __future__ import print_function
import brickpi
import math
import time
from ConfigParser import RawConfigParser
from eventTypes import EventType, EventState
from motor import Motor
from sensor import PushSensor, Bumper , UltraSonicSensor

"""
A much simplified event handler class. Just add events and raise them by name
"""
class Events:
	data = {}
	
	"""
	Adds an event to the list identified by `name`.
	When `invoke(name, params)` is called, every event added with this
	function will be called with `event(params)`. `params` is typically
	a dictionary with named values, such as 'position', 'state' etc.
	"""
	def add(self, name, event):
		if self.data.get(name) is None:
			self.data[name] = [event]
		else:
			self.data[name].append(event)

	"""
	Raises the event identified by `name`
	e.g. a sensor might call `invoke(SENSOR_TYPE_FOO, {'value':self.value})`
	"""
	def invoke(self, name, params):
		if self.data.get(name) is None:
			return
		for handler in self.data.get(name):
			handler(params)

"""
Main robot class
"""	
class Robot:

	######################
	### Initialisation ###
	######################

	"""
	Sets up the standard motor parameters (excluding PID values)
	"""
	def initMotorParams(self, motorParams):
		motorParams.maxRotationAcceleration = 10
		motorParams.maxRotationSpeed = 20
		motorParams.feedForwardGain = 255/20
		motorParams.minPWM = 18
		motorParams.pidParameters.minOutput = -255
		motorParams.pidParameters.maxOutput = 255
	
	"""
	Reads robot configuration from the config file
	"""
	def initConfig(self):
		config = RawConfigParser()
		config.optionxform = str
		config.read('robot.cfg')
		for (item, value) in config.items('Robot'):
			setattr(self, item, float(value))
		print("Robot config loaded")
	
	"""
	Sets default configuration values - call this before `initConfig`
	"""
	def setDefaults(self):
		# The time between successive `check` calls
		self.deltaTime = 0.1
		# Overall power coefficient to the motors
		self.powerL = 1
		self.powerR = 1
		# Overall coefficient for rotation
		self.rotatePower = 0.95

		# Number of radians to one metre of movement
		self.movementCoeff = 36.363636
		# The centre-to-wheel distance of the robot
		self.botRadius = 0.08
		
		# Motor PID values
		self.pidk_p = 600
		self.pidk_i = 100
		self.pidk_d = 20

	def __init__(self):
		self.logging = False
		self.isLogging = False
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
		Bumper(self.events)
		self.ultraSonic = UltraSonicSensor(self.interface, 2, self.events, brickpi.SensorType.SENSOR_ULTRASONIC)
		self.setPID(self.pidk_p, self.pidk_i, self.pidk_d)

		self.events.add(EventType.SENSOR_TOUCH, self.sensorAction)
	
	###############
	### Logging ###
	###############

	"""
	Set whether to enable logging
	"""
	def setLogging(self, log):
		self.logging = log

	"""
	Starts logging on the current interface
	`optargs` is a list of identifying values for the log file name
	"""
	def startLogging(self, optargs):
		if self.logging:
			self.isLogging = True
			optargs = [optarg for optarg in optargs if optarg is not None]
			optargs_str = '_'.join(str(optarg) for optarg in optargs)
			self.logName = './logs/' + \
				str(int(time.time())) +'_p' + \
				str(self.pidk_p) + '_i' + \
				str(self.pidk_i) + '_d' + \
				str(self.pidk_d) + '_' + optargs_str + '.log'
			self.interface.startLogging(self.logName)

	"""
	Stops all logging
	"""
	def stopLogging(self):
		if self.isLogging:
			self.isLogging = False
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
	
	"""
	Sets PID values for all motors
	"""
	def setPID(self, p, i, d):
		self.motorL.setPID(p, i, d)
		self.motorR.setPID(p, i, d)
	
	"""
	Whether any of the motors are rotating
	"""
	def isMoving(self):
		return self.motorL.isRotating() or self.motorR.isRotating()

	"""
	Moves the given distance forwards or backwards
	"""
	def move(self, distance):
		# distance specified in metres
		wheel = distance * self.movementCoeff
		self.startLogging(['move', distance])
		self.motorL.rotate(self.powerL * wheel)
		self.motorR.rotate(self.powerR * wheel)
		self.stopLogging()
	
	"""
	Rotates the whole robot by the given angle clockwise
	"""
	def rotate(self, angle):
		# angle specified in degrees
		wheel = self.rotatePower * angle * (math.pi/180) * self.botRadius * self.movementCoeff
		self.startLogging(['turn', angle])
		self.motorL.rotate( self.powerL * wheel)
		self.motorR.rotate(-self.powerR * wheel)
		self.stopLogging()

	def drive(self, speedL, speedR):
		self.motorL.setSpeed(speedL)
		self.motorR.setSpeed(speedR)

	def arcPath(self, theta):
		# theta = 0 returns to straight path
		# Positive theta => too far to the right => turn left
		if theta <= 0 :
			self.powerL = 1 
			self.powerR = 1 + theta
		else: 		
			self.powerL = 1 - theta
			self.powerR = 1 
	
	"""
	Blocks the program until the robot stops moving
	"""
	def wait(self):
		while self.isMoving():
			time.sleep(self.deltaTime)

	######################
	### Sensor control ###
	######################

	"""
	Starts the main loop, checking sensors and responding to events until
	`running` is false
	"""
	def mainLoop(self):
		self.running = True
		while self.running:
			self.touchSensorL.check()
			self.touchSensorR.check()
			self.ultraSonic.check()
			self.motorL.check()
			self.motorR.check()
			time.sleep(self.deltaTime)

	def sensorAction(self, params):
		if(params['position'] != 'either' or not params['down']):
			return
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
		

			
