from robot import Robot
import brickpi
import time

print("START")
robot = Robot()

port = 2 # port which ultrasoic sensor is plugged in to
robot.interface.sensorEnable(port, brickpi.SensorType.SENSOR_ULTRASONIC);

while True:
	sensor_distance_h = robot.interface.getSensorValue(port)
	print("Distance:",sensor_distance_h)
	robot.wait()
	