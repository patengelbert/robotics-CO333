from robot import Robot
from math import atan2, sqrt, degrees, fabs

class Navigate:

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
		angle = degrees(atan2(disty, distx))
		rotation = angle - self.theta
		while rotation > 180:
			rotation -= 360
		while rotation < -180:
			rotation += 360

		print 'Rotating: ' + str(rotation) +\
			 ' to heading ' + str(angle)
		self.robot.rotate(rotation)
		self.robot.wait()
		distance = sqrt((distx ** 2) + (disty ** 2))
		
		#Either move directly to the way point or in steps
		if step == 0 || distance <= step:
			self.robot.move(distance)
		else 
			distance = step
			self.robot.move(distance)
		
		print 'Travelling: ' + str(distance) +\
				 'm to location ' + str(point)
		self.robot.wait()
		
		#TODO correct position to work with mcl
		updatePosition(distance, rotation)
		
	def updatePosition(self, d, a):
		# Update the current position
		self.theta += a
		self.x = d*cos(p.a)
		self.y = d*sin(p.a)

if __name__ == '__main__':
	robot = Robot()
	navigate = Navigate(robot)
	while True:
		print('Enter waypoint coordinate')
		pointX = input('x:')
		pointY = input('y:')
		navigate.waypoint((pointX, pointY))
			
