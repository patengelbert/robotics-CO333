# encoding=utf8

from robot import Robot
import brickpi
import time

#Lab 2 Wall Following -- Simplified as there's no fucking mention of the word event in the entirity of the bleeding handout.

sensor_left_side = bool(input("Which way is the sensor pointing?\nRight:0\nLeft:1\n"))
print("Wall Following Initiated (Ctrl+C to close)")
robot = Robot()

port = 2 # port which ultrasoic sensor is plugged in to
robot.interface.sensorEnable(port, brickpi.SensorType.SENSOR_ULTRASONIC);
turn_gain = 3/100 #Fine Tuning Required. Max distance from wall is 30 + (turn_gain-1)

while True:
	sensor_distance_h = robot.interface.getSensorValue(port)
	sensor_distance= sensor_distance_h[0]
	print "Sensor Distance: ",sensor_distance
	if  (abs((sensor_distance-30)*turn_gain)) <=1:
		if sensor_left_side:
			robot.arcPath(turn_gain*(sensor_distance-30))
		else:
			robot.arcPath(turn_gain*(30-sensor_distance))
		print  "Robot.move reached"
		robot.move(0.1)
		robot.wait()
	else:
		print("Too far from the wall")
		robot.arcPath(0)
		if sensor_left_side:
			robot.rotate(-90)
			robot.wait()
			robot.move(0.2)
			robot.wait()
			robot.rotate(90)
		else:
			robot.rotate(90)
			robot.wait()
			robot.move(0.2)
			robot.wait()
			robot.rotate(-90)
		time.sleep(0.5)
