from robot import Robot
from math import cos, sin
import random

class Particle:
	def __init__(self, x, y, a):
		self.x = x
		self.y = y
		self.a = a

class ProbabilisticMotion:

	mean = 0
	sd = 0.1
	step = 0.1
	size = 0.4
	numParticles = 100
	
	def __init__(self, robot):
		self.robot = robot
		self.particles = [Particle(0, 0, 0)]*self.numParticles

	def noise(self):
		return random.random()*0.05

	def updateParticles(self, d):
		particles = [Particle(\
			p.x + (d + self.noise())*cos(p.a), \
			p.y + (d + self.noise())*sin(p.a), \
			p.a + self.noise()) for p in self.particles]

	def updateAngle(self, a):
		particles = [Particle(p.x, p.y, p.a + a + self.noise()) \
			for p in self.particles]

	def run(self):
		posX = 0
		posY = 0
		angle = 0
		for i in range(0, 4):
			total = 0.0
			while total < self.size:
				robot.move(self.step)
				robot.wait()
				updateParticles(self.step)
				print("drawParticles:" + str(self.particles))
				newX += step*cos(angle)
				newY += step*sin(angle)
				print("drawLine:" + str(posX, posY, newX, newY))
				posX = newX
				posY = newY
			robot.rotate(90)
			robot.wait()
			updateAngle(90)
			print("drawParticles:" + str(self.particles))
			angle += 90

if __name__ == '__main__':
	robot = Robot()
	robot.setPID(150, 0, 0)
	motion = ProbabilisticMotion(robot)
	motion.run()

