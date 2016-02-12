import brickpi
import math
from ConfigParser import RawConfigParser
from eventTypes import EventType

class Motor:

	def __init__(self, interface, events, id):
		self.interface = interface
		self.events = events
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
		print("Motor " + str(self.id) + " Config loaded")

	def setPID(self, p, i, d):
		self.motorParams.pidParameters.k_p = p
		self.motorParams.pidParameters.k_i = i
		self.motorParams.pidParameters.k_d = d
		self.updateParams()
		
	def updateParams(self):
		self.interface.setMotorAngleControllerParameters(self.id, self.motorParams)

	def rotate(self, angle):
		self.interface.increaseMotorAngleReference(self.id, angle)
		self.wasRotating = True

	def isRotating(self):
		return math.fabs(self.interface.getMotorAngleReferences([self.id])[0] - self.interface.getMotorAngle(self.id)[0]) > self.threshold

	def check(self):
		if(self.wasRotating and not self.isRotating()):
			self.wasRotating = False
			self.events.invoke(EventType.MOTOR_STOP, {})
