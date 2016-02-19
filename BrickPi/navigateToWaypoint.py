from robot import Robot
from math import atan2, sqrt, degrees, fabs

class Navigate:

	def __init__(self, robot):
		self.robot = robot
		self.x = 0
		self.y = 0
		self.theta = 0

	def waypoint(self, point):
		if point == (self.x, self.y):
			return
		(targetx, targety) = point
		distx = targetx - self.x
		disty = targety - self.y
		angle = degrees(atan2(disty, distx))
		rotation = angle - self.theta
		if fabs(rotation) > 180:
			rotation = rotation - 360
		print 'Rotating: ' + str(rotation) +\
			 ' to heading ' + str(angle)
		self.robot.rotate(rotation)
		self.robot.wait()
		distance = sqrt((distx ** 2) + (disty ** 2))
		print 'Travelling: ' + str(distance) +\
			 'm to location ' + str(point)
		self.robot.move(distance)
		self.robot.wait()
	
		# Update the current position
		self.theta = angle
		self.x = targetx
		self.y = targety

if __name__ == '__main__':
	robot = Robot()
	navigate = Navigate(robot)
	navigate.waypoint((0.1,0.1))
	navigate.waypoint((0, 0))
	navigate.waypoint((-0.1, 0.0))
	navigate.waypoint((0.1, 0.1))

