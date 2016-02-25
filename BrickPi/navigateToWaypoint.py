from robot import Robot
from math import atan2, sqrt, degrees, fabs

class Navigate(object):

	def __init__(self, robot):
		self.robot = robot
		self.x = 0
		self.y = 0
		self.theta = 0
		self.error = False

	def waypoint(self, point, step=0):
		if self.error:
			self.error = not self.updatePosition(0, 0)
			return;
		if point == (self.x, self.y):
			return
		(targetx, targety) = point
		distx = targetx - self.x
		disty = targety - self.y
		angle = atan2(disty, distx)
		rotation = angle - self.theta
		while rotation > math.pi:
			rotation -= 2*math.pi
		while rotation < -math.pi:
			rotation += 2*math.pi

		print 'Rotating: ' + str(degrees(rotation)) +\
			 ' to heading ' + str(degrees(angle))
		self.robot.rotate(degrees(rotation))
		self.robot.wait()
		distance = sqrt((distx ** 2) + (disty ** 2))
		
		#Either move directly to the way point or in steps
		if step == 0 or distance <= step:
			self.robot.move(distance)
		else: 
			distance = step
			self.robot.move(distance)
		
		print 'Travelling: ' + str(distance) +\
				 'm to location ' + str(point)
		self.robot.wait()
		
		#TODO correct position to work with mcl
		self.error = not self.updatePosition(distance, rotation)
		
	def updatePosition(self, d, a):
		# Update the current position
		self.theta += a
		self.x = d*cos(p.a)
		self.y = d*sin(p.a)
		return True

if __name__ == '__main__':
	robot = Robot()
	navigate = Navigate(robot)
	while True:
		print('Enter waypoint coordinate')
		pointX = input('x:')
		pointY = input('y:')
		navigate.waypoint((pointX, pointY))
			
