import brickpi
import math
import time

class Motor:
	threshold = 0.5

	def __init__(self, interface, id):
		self.interface = interface
		self.id = id
		self.motorParams = interface.MotorAngleControllerParameters()
		interface.motorEnable(id)

	def setPID(p, i, d):
		motorParams.pidParameters.k_p = p
		motorParams.pidParameters.k_i = i
		motorParams.pidParameters.k_d = d
		update()
		
	def update():
		interface.setMotorAngleControllerParameters(id, motorParams)

	def rotate(angle):
		interface.increaseMotorAngleReference(id, angle)

	def isRotating():
		return math.abs(interface.getMotorAngleReference(id) - interface.getMotorAngle(id)) > threshold

class Robot:
	powerL = 1
	powerR = 1
	rotatePower = 1

	movementCoeff = 0.36
	botRadius = 0.16
	
	def initMotorParams(motorParams):
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
		initMotorParams(self.motorL.motorParams)
		initMotorParams(self.motorR.motorParams)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.interface.terminate()
	
	def setPID(p, i, d):
		motorL.setPID(p, i, d)
		motorR.setPID(p, i, d)
	
	def isMoving():
		return motorL.isRotating() or motorR.isRotating()
	
	def move(distance):
		wheel = (distance * (180/math.pi)) * movementCoeff;
		motorL.rotate(powerL * wheel)
		motorR.rotate(powerR * wheel)
	
	def rotate(angle):
		wheel = rotatePower * angle * botRadius * movementCoeff;
		motorL.rotate( powerL * wheel)
		motorR.rotate(-powerR * wheel)
	
	def wait():
		while isMoving():
			time.sleep(0.1)

