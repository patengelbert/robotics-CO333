from robot import Robot

repeats = int(input("Number of squares: "))
size = float(input("Size of square (m): "))
rot = bool(input("Anticlockwise?: ))
with Robot() as robot:
	for i in range(0, repeats):
		for i in range(0, 4):
			robot.move(size)
			robot.wait()
			if rot:
				robot.rotate(90)
			else:
				robot.rotate(-90)
			robot.wait()

