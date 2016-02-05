from robot import Robot

#Lab 1 Section 5.3

testchoice = int(input("Tests\nStraight:0\nRotation:1\nStandard Request:2\n"))

if testchoice == 0:
	size = float(input("Intended Travel Distance (m):\n"))
	robot.move(size)
	robot.wait()
	robot.move(-size)
	robot.wait()
elif testchoice == 1:
	angle = float(input("Intended Rotation (degrees):\n"))
	robot.rotate(angle)
	robot.wait()
	robot.rotate(-angle)
	robot.wait()
else:
	robot.move(0.4)
	robot.wait()
	robot.move(-0.4)
	robot.wait()
	robot.rotate(90)
	robot.wait()
	robot.rotate(-90)
	robot.wait()


			