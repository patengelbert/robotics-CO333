from robot import Robot
from math import tan, sqrt, degrees

class Navigate:
	def __init__(self, robot):
		self.robot = robot
		self.x = 0
		self.y = 0
		self.theta = 0
	def waypoint(self, point):
		(targetx, targety) = point
		angle = degrees(tan(targety/targetx))
		rotation = self.theta - angle
		if rotation > 180:
			robot.rotate(360 - rotation)
		elif rotation < -180:
			robot.rotate(360 + rotation)
		else:
			robot.rotate(rotation)
		print rotation
		robot.wait()
		self.theta = angle
		distx = targetx - self.x
		disty = targety - self.y
		distance = sqrt((distx ** 2) + (disty ** 2))
		print distance
		robot.move(distance)
		robot.wait()
		self.x = targetx
		self.y = targety

if __name__ == '__main__':
	robot = Robot()
	navigate = Navigate(robot)
	while true:
		print('Enter waypoint coordinate')
		pointX = input('x:')
		pointY = input('y:')
		navigate.waypoint((pointX, pointY))
			
		
