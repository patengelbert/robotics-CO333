import brickpi
import time

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
motorParams.pidParameters.k_i = 130
motorParams.pidParameters.k_d = 12

interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)

while True:
	decision = int(input("Option 0: Straight \n Option 1: Rotate \n "))
	angle = float(input("Enter a angle to rotate (in radians): "))
	interface.startLogging('logs/log' +str(motorParams.pidParameters.k_p) + '.txt')
    
	if decision == 0:
		interface.increaseMotorAngleReferences(motors,[angle,angle])
	else:
		interface.increaseMotorAngleReferences(motors,[(-1*angle),angle])

	while not interface.motorAngleReferencesReached(motors) :
		motorAngles = interface.getMotorAngles(motors)
		if motorAngles :
			print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
		time.sleep(0.2)

	print "Destination reached! Allahu Akbar"
	interface.stopLogging()



interface.terminate()
