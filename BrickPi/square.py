import brickpi
import time
import math

global interface #Global variables
global motors #AKA lazy programming

def completesquare(diameter): # Draws a square
	for i in range(0,4): 
		straight(diameter) #Edge
		rotatedeg(90,0) #Corner

def straight(drivedist): #  Drive in straight line in cm
	#35 rads per metre = 0.35 per cm
	drive_rad_const = 0.36 # Converts cm into wheel rotations
	angle = drivedist * drive_rad_const 
	print angle
	interface.increaseMotorAngleReferences(motors,[angle,angle])
	while not interface.motorAngleReferencesReached(motors) :
		time.sleep(0.1)

def rotatedeg(degrees,clockwise):
	rotate_const = 2.8 #Converts degrees into wheel rotations
	angle = degrees *  rotate_const * math.pi/180
	if clockwise == 1:
		interface.increaseMotorAngleReferences(motors,[(-1*angle),angle])
	else:
		interface.increaseMotorAngleReferences(motors,[angle,(-1*angle)])
	while not interface.motorAngleReferencesReached(motors) :
		time.sleep(0.1)

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
	motorParams.pidParameters.k_p = 600
	motorParams.pidParameters.k_i = 500
	motorParams.pidParameters.k_d = 20

	interface.setMotorAngleControllerParameters(motors[0],motorParams)
	interface.setMotorAngleControllerParameters(motors[1],motorParams)

#Main

interface = brickpi.Interface() #Initialisation
interface.initialize() 
motors = [0,1]
PIDparams()

while True:
	diameter = int(input("Enter square perimeter (in cm) \n "))
	
	completesquare(diameter)
	
	print "Enjoy your fucking square!"



interface.terminate()
