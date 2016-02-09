import brickpi
import math
import time

from ConfigParser import RawConfigParser
from events import Events as Event

class Motor:

	def __init__(self, interface, id):
		self.interface = interface
		self.id = id
		self.motorParams = interface.MotorAngleControllerParameters()
		self.threshold = 0.05
		self.initConfig()
		interface.motorEnable(id)

	def initConfig(self):
		config = RawConfigParser()
		config.optionxform = str
		config.read('robot.cfg')
		for (item, value) in config.items('Motor'):
			setattr(self, item, float(value))
		print "Motor " + str(self.id) + " Config loaded"

	def setPID(self, p, i, d):
		self.motorParams.pidParameters.k_p = p
		self.motorParams.pidParameters.k_i = i
		self.motorParams.pidParameters.k_d = d
		self.updateParams()
		
	def updateParams(self):
		self.interface.setMotorAngleControllerParameters(self.id, self.motorParams)

	def rotate(self, angle):
		self.nextMove = angle
		#self.interface.increaseMotorAngleReference(self.id, angle)

	def isRotating(self):
		return math.fabs(self.interface.getMotorAngleReferences([self.id])[0] - self.interface.getMotorAngle(self.id)[0]) > self.threshold

class Sensor:
	
	def __init__(self, interface, port, eventManager, sensorType):
		self.interface = interface
		self.port = port
		self.eventManager = eventManager
		try:
			self.event = Event()
			self.eventManager.registerEvent(str(self.sensorType), self.event)
		except KeyError as e:
			self.event = eventManager.getEvent(str(self.sensorType)
		interface.sensorEnable(port, self.sensorType)

	def check(self) = None

class PushSensor(Sensor):

	def __init__(self, position, *args, **kwargs):
		self.position = position
		super(PushSensor, self)__init__(*args, **kwargs)
		self.value = False

	def check(self):
		cvalue = self.interface.getSensorValue(self.port)
		if(self.value != cvalue):
			self.event.on_event({'position':self.position, 'state':cvalue})
			self.value = cvalue

class EventManager:
	
	def __init__(self):
		self.events = {}
	
	def getEventList(self):
		return self.events.keys()
	
	def getEvent(self, name):
		if self.events.get(name) is None:
			raise KeyError('Event %s has not been registered'% name)
		return self.events[name]
	
	def registerEvent(self, name, event):
		if self.events.get(name) is not None:
			raise KeyError('Event %s has already been registered'% name)
		self.events[name] = event

	def unregisterEvent(self, name):
		if self.events.get(name) is None:
			raise KeyError('Event %s has not been registered'% name)
		self.events.pop(name)

	def registerHandler(self, name, handler):
		if self.events.get(name) is None:
			raise KeyError('Event %s has not been registered'% name)
		self.events[name] += handler		
	
class Robot:
	
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
		print "Robot config loaded"
	
	def setDefaults(self):
	
		# Default config values
		self.powerL = 1
		self.powerR = 1
		self.rotatePower = 0.95

		self.movementCoeff = 36.363636
		self.botRadius = 0.08
		
		self.pidk_p = 600
		self.pidk_i = 400
		self.pidk_d = 20

	def __init__(self):
		self.setDefaults()
		self.interface = brickpi.Interface()
		self.interface.initialize()
		self.eventManager = EventManager()
		self.motorL = Motor(self.interface, 0)
		self.motorR = Motor(self.interface, 1)
		self.initMotorParams(self.motorL.motorParams)
		self.initMotorParams(self.motorR.motorParams)

		self.initConfig()
		self.touchSensorL = PushSensor(interface=self.interface, port=1, sensorType=brickpi.SensorType.SENSOR_TOUCH, position='left', eventManager=self.eventManager)
		self.touchSensorR = PushSensor(interface=self.interface, port=2, sensorType=brickpi.SensorType.SENSOR_TOUCH, position='right', eventManager=self.eventManager)
		self.setPID(self.pidk_p, self.pidk_i, self.pidk_d)

		self.eventManager.registerHandler(str(brickpi.SensorType.SENSOR_TOUCH), lambda params: print(str(params)));
	
	def setLogging(self, log):
		self.logging = log

	def setLogName(self, optargs = None):
		optargs = [optarg for optarg in optargs if optarg is not None]
		optargs_str = '_'.join(str(optarg) for optarg in optargs)
		self.logName = './logs/' + str(int(time.time())) +'_p' + str(self.pidk_p) + '_i' + str(self.pidk_i) + '_d' + str(self.pidk_d) + '_' + optargs_str + '.log'

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.interface.terminate()
	
	def setPID(self, p, i, d):
		self.motorL.setPID(p, i, d)
		self.motorR.setPID(p, i, d)
	
	def isMoving(self):
		return self.motorL.isRotating() or self.motorR.isRotating()
	
	def move(self, distance):
		wheel = distance * self.movementCoeff;
		self.motorL.rotate(self.powerL * wheel)
		self.motorR.rotate(self.powerR * wheel)
		if self.logging:
			self.setLogName(['move', distance])
			self.interface.startLogging(self.logName)			
		self.startAction()
		if self.logging:
			pass
			self.interface.stopLogging()
	
	def rotate(self, angle):
		wheel = self.rotatePower * angle * (math.pi/180) * self.botRadius * self.movementCoeff;
		self.motorL.rotate( self.powerL * wheel)
		self.motorR.rotate(-self.powerR * wheel)
		if self.logging:
			self.setLogName(['turn', angle])
			self.interface.startLogging(self.logName)			
		self.startAction()
		if self.logging:
			self.interface.stopLogging()

	def startAction(self):
		self.interface.increaseMotorAngleReferences([self.motorL.id, self.motorR.id], [self.motorL.nextMove, self.motorR.nextMove])
	
	def wait(self):
		while self.isMoving():
			time.sleep(0.1)

	def mainLoop(self):
		while True:
			self.touchSensorL.check()
			self.touchSensorR.check()

			
