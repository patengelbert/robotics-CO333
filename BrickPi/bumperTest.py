from robot import Robot

with Robot() as robot:
	while True:
		robot.checkSensors()
		robot.move(5)
