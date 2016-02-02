import brickpi
import time
import math

def completesquare(diameter):
	for i in range(0,3):
		straight(diameter)
		rotatedeg(90,0)

def straight(drivedist):
	diameter_rad_const = 1
	angle = drivedist * diameter_rad_const
	interface.increaseMotorAngleReferences(motors,[angle,angle])

def rotatedeg(degrees,clockwise):
	rads = degrees*pi/180
	rotate_const = 1
	angle = rads *  rotate_const
	if clockwise == 1:
		interface.increaseMotorAngleReferences(motors,[(-1*angle),angle])
	else:
		interface.increaseMotorAngleReferences(motors,[angle,(-1*angle)])
		
interface=brickpi.Interface()
interface.initialize()

motors = [0,1]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParams = interface.MotorAngleControllerParameters()
motorParams.maxRotationAcceleration = 10.0
motorParams.maxRotationSpeed = 20.0
motorParams.feedForwardGain = 255/20.0
motorParams.minPWM = 18.0
motorParams.pidParameters.minOutput = -255
motorParams.pidParameters.maxOutput = 255
motorParams.pidParameters.k_p = 120
motorParams.pidParameters.k_i = 150
motorParams.pidParameters.k_d = 12

interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)

while True:
	diameter = int(input("Enter square perimeter (in cm) \n "))
	
	completesquare(diameter)
	
	print "Enjoy your fucking square!"
	interface.stopLogging()



interface.terminate()
