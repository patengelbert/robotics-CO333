from robot import Robot

repeats = int(input("Number of squares: "))
size = float(input("Size of square (m): "))
with Robot() as robot:
	robot.setLogging(True)
	for i in range(0, repeats):
		for i in range(0, 4):
			robot.move(size)
			robot.wait()
			robot.rotate(90)
			robot.wait()

