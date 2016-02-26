from robot import Robot
from math import atan2, sqrt, degrees, fabs, pi, sin, cos, radians

class Navigate(object):

	def __init__(self, robot):
		self.robot = robot
		self.x = 0
		self.y = 0
		self.theta = 0
		self.error = False

	def waypoint(self, point, step=0):
		#if self.error:
			#self.error = not self.updatePosition(0, 0)
			#targetx = self.x + (10*cos(self.theta))
			#targety = self.y + (10*sin(self.theta))
			#return
		if point == (self.x, self.y):
			return
		
		(targetx, targety) = point
		distx = targetx - self.x
		disty = targety - self.y
		angle = atan2(disty, distx)
		while angle > pi:
			angle -= 2*pi
		while angle <= -pi:
			angle += 2*pi
		rotation = angle - self.theta
		print ('targetx: ' + str(targetx) + ', targety: ' + str(targety) + ', distx = ' + str(distx) + ', disty: ' + str(disty) + ', x: ' + str(self.x) + ', y: ' + str(self.y))
		print ('angle: ' + str(angle) + ', theta: ' + str(self.theta) + ', rotation: ' + str(rotation))
		while rotation > pi:
			print 'angle overflow'
			rotation -= 2*pi
		while rotation <= -pi:
			rotation += 2*pi
			print 'angle overflow2'
		print 'Rotating: ' + str(degrees(rotation)) +\
			 ' from '+ str(self.theta) + ' to heading ' + str(degrees(angle))
		self.robot.rotate(degrees(rotation))
		self.robot.wait()
		
		distance = sqrt((distx ** 2) + (disty ** 2))
		
		#Either move directly to the way point or in steps
		if step == 0 or distance <= step:
			pass
		else: 
			distance = step
		self.robot.move(distance)
		
		print 'Travelling: ' + str(distance) +\
				 'm to location ' + str(point)
		
		self.robot.wait()
		
		#TODO correct position to work with mcl
		self.error = not self.updatePosition(distance, angle)
		
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
			
