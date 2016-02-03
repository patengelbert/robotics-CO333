import brickpi
import math
import time

class Motor:
	threshold = 0.1

	def __init__(self, interface, id):
		self.interface = interface
		self.id = id
		self.motorParams = interface.MotorAngleControllerParameters()
		interface.motorEnable(id)

	def setPID(self, p, i, d):
		self.motorParams.pidParameters.k_p = p
		self.motorParams.pidParameters.k_i = i
		self.motorParams.pidParameters.k_d = d
		self.update()
		
	def update(self):
		self.interface.setMotorAngleControllerParameters(self.id, self.motorParams)

	def rotate(self, angle):
		self.interface.increaseMotorAngleReference(self.id, angle)

	def isRotating(self):
		return math.fabs(self.interface.getMotorAngleReferences([self.id])[0] - self.interface.getMotorAngle(self.id)[0]) > self.threshold

class Robot:
	powerL = 1
	powerR = 1
	rotatePower = 1

	movementCoeff = 36.363636
	botRadius = 0.08
	
	def initMotorParams(self, motorParams):
		motorParams.maxRotationAcceleration = 10
		motorParams.maxRotationSpeed = 20
		motorParams.feedForwardGain = 255/20
		motorParams.minPWM = 18
		motorParams.pidParameters.minOutput = -255
		motorParams.pidParameters.maxOutput = 255

	def __init__(self):
		self.interface = brickpi.Interface()
		self.interface.initialize()
		self.motorL = Motor(self.interface, 0)
		self.motorR = Motor(self.interface, 1)
		self.initMotorParams(self.motorL.motorParams)
		self.initMotorParams(self.motorR.motorParams)

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
	
	def rotate(self, angle):
		wheel = self.rotatePower * angle * (math.pi/180) * self.botRadius * self.movementCoeff;
		self.motorL.rotate( self.powerL * wheel)
		self.motorR.rotate(-self.powerR * wheel)
	
	def wait(self):
		while self.isMoving():
			time.sleep(0.1)

