import brickpi
import time
import math

def completesquare(diameter): # Draws a square
	for i in range(0,3): 
		straight(diameter) #Edge
		rotatedeg(90,0) #Corner

def straight(drivedist): #  Drive in straight line in cm
	drive_rad_const = 1 # Converts cm into wheel rotations
	angle = drivedist * drive_rad_const 
	interface.increaseMotorAngleReferences(motors,[angle,angle])

def rotatedeg(degrees,clockwise):
	rotate_const = 1 #Converts degrees into wheel rotations
	angle = rads *  rotate_const *pi/180
	if clockwise == 1:
		interface.increaseMotorAngleReferences(motors,[(-1*angle),angle])
	else:
		interface.increaseMotorAngleReferences(motors,[angle,(-1*angle)])
		
def PIDparams():
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
	motorParams.pidParameters.k_i = 130
	motorParams.pidParameters.k_d = 12

	interface.setMotorAngleControllerParameters(motors[0],motorParams)
	interface.setMotorAngleControllerParameters(motors[1],motorParams)

global interface #Global variables
global motors

interface = brickpi.Interface() #Initialisation
interface.initialize() 
motors = [0,1]
PIDparams()

while True:
	diameter = int(input("Enter square perimeter (in cm) \n "))
	
	completesquare(diameter)
	
	print "Enjoy your fucking square!"
	interface.stopLogging()



interface.terminate()
