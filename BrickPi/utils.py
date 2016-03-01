from math import pi

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Particle:
	def __init__(self, x, y, a, p=1):
		self.x = x
		self.y = y
		self.a = a
		self.p = p

	def __str__(self):
		return self.x, self.y, self.a, self.p

def clampAngle(angle):
	while angle > pi:
		angle -= 2*pi
	while angle <= -pi:
		angle += 2*pi
	return angle

def clampAnglePositive(angle):
	while angle < 0:
		angle += 2*pi
	while angle > 2*pi:
		angle -= 2*pi

