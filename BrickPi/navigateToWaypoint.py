from robot import Robot
from math import atan2, sqrt, degrees, fabs, pi, sin, cos, radians
from utils import clampAngle

class Navigate(object):

	def __init__(self, robot):
		self.robot = robot
		self.x = 0
		self.y = 0
		self.theta = 0

	def waypoint(self, point, step=0):
		if point == (self.x, self.y):
			return
		
		(targetx, targety) = point
		distx = targetx - self.x
		disty = targety - self.y
		angle = clampAngle(atan2(disty, distx))
		rotation = clampAngle(angle - self.theta)
		if self.robot.debug:
			print 'Rotating ' + str(degrees(rotation)) +\
			 ' from '+ str(degrees(self.theta)) + ' to heading ' + str(degrees(angle))
		self.robot.rotate(degrees(rotation))
		self.robot.wait()
		
		distance = sqrt((distx ** 2) + (disty ** 2))
		
		#Either move directly to the way point or in steps
		if step != 0 and distance > step:
			distance = step
		self.robot.move(distance)
		
		if self.robot.debug:
			print 'Travelling ' + str(distance) +\
				 'm to location ' + str(point)
		self.robot.wait()
		self.updatePosition(distance, rotation)
		
	def updatePosition(self, d, a):
		self.theta = clampAngle(self.theta + a)
		self.x += d*cos(self.theta)
		self.y += d*sin(self.theta)
		return True

if __name__ == '__main__':
	robot = Robot()
	navigate = Navigate(robot)
	while True:
		print('Enter waypoint coordinate')
		pointX = input('x:')
		pointY = input('y:')
		navigate.waypoint((pointX, pointY))
			
