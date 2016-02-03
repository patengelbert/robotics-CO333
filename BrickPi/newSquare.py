import robot

size = int(input("Size of square (m): "))
with Robot() as robot:
	robot.setPID(600, 500, 20)
	for i in range(0, 3):
		robot.move(size)
		robot.wait()
		robot.rotate(90)
		robot.wait()

