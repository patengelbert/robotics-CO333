import brickpi
import math
from ConfigParser import RawConfigParser
from eventTypes import EventType

"""
A single motor
"""
class Motor:

	def __init__(self, interface, events, id):
		self.interface = interface
		self.events = events
		self.id = id
		self.motorParams = interface.MotorAngleControllerParameters()
		self.threshold = 0.05 # 'Close enough' angle
		self.initConfig()
		self.wasRotating = False
		interface.motorEnable(id)

	"""
	Reads configuration data from file
	"""
	def initConfig(self):
		config = RawConfigParser()
		config.optionxform = str
		config.read('robot.cfg')
		for (item, value) in config.items('Motor'):
			setattr(self, item, float(value))
		print("Motor " + str(self.id) + " Config loaded")

	"""
	Sets the PID parameters
	"""
	def setPID(self, p, i, d):
		self.motorParams.pidParameters.k_p = p
		self.motorParams.pidParameters.k_i = i
		self.motorParams.pidParameters.k_d = d
		self.updateParams()
	
	"""
	Applies changes made to `motorParams`
	"""	
	def updateParams(self):
		self.interface.setMotorAngleControllerParameters(self.id, self.motorParams)

	"""
	Rotates the motor by the given angle
	"""
	def rotate(self, angle):
		self.interface.increaseMotorAngleReference(self.id, angle)
		self.wasRotating = True

	"""
	Whether the motor is currently rotating; i.e. has not reached its reference
	"""
	def isRotating(self):
		angleRef = self.interface.getMotorAngleReferences([self.id])
		if(angleRef == []):
			return False
		return math.fabs(angleRef[0] \
		- self.interface.getMotorAngle(self.id)[0]) > self.threshold

	"""
	Sets the motor to the given speed in radians/second
	"""
	def setSpeed(self, speed):
		self.interface.setMotorRotationSpeedReferences([self.id], [speed])
	
	"""
	Calls events as necessary
	"""
	def check(self):
		if(self.wasRotating and not self.isRotating()):
			self.wasRotating = False
			self.events.invoke(EventType.MOTOR_STOP, {})

