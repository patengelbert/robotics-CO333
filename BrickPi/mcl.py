from robot import Robot
from navigateToWaypoint import Navigate
import random
from math import exp, fabs, isinf
from eventTypes import EventType


class MonteCarloWaypoint(Navigate):
	
	numParticles = 100

	def __init__(self, robot):
		super(Navigate).__init__(self, robot)
		
		#init for navigation
		self.step = 20
		self.particles = [Particle(0, 0, 0, 1/self.numParticles)]*self.numParticles
	
	def run(self):
		running = true
		while running:
			print('Enter waypoint coordinate')
			pointX = input('x:')
			pointY = input('y:')
			
			while self.x != pointX and self.y != pointY:
				self.waypoint((pointX, pointY), self.step)
				updatePoints()
			

	def updatePosition(self, d, a):
		# Redo weightings
		self.particles = [Particle(\
			p.x + (d + self.noise())*cos(p.a), \
			p.y + (d + self.noise())*sin(p.a), \
			p.a + self.noise() + a, \
			p.p * calculate_likelihood(p.x, p.y, p.a, self.depth))\
			for p in self.particles] 
		# Resample high values and cull low values
		self.particles = resample(self.particles)
		# Normalise Weightings
		self.particles = normalise(self.particles)
		tX = 0
		tY = 0
		tA = 0
		for p in self.particles:
			tX += p.x
			tY += p.y
			tA += p.a
		#Update the current position
		self.theta = tA/self.numParticles
		self.x = tX/self.numParticles
		self.y = tY/self.numParticles


	def normalise(self, particles):
		tWeight = 0
		for p in particles:
			tWeight += p.p
		return [Particle(\
			p.x, p.y, p.a,\
			p.p / tWeight) \
			for p in particles]
		
	def calculate_likelihood(self, x, y, theta, z):
		estimateDepth = getMappedDepth()
		measuredDepth = z
		if not isinf(measuredDepth):
			exponent = fabs(estimatedDepth - measuredDepth)
			return exp(-1 * exponent)
		else:
			return 1
		
	def resample(self):
		newParticles = [Particle(0, 0, 0)]*self.numParticles
		
		#generate cumulative weight array
		cumulativeWeight = [0]*self.numParticles
		for i, tempParticle in self.particles
			sum = 0
			for j in range(0,i)
				sum += self.particle[j].p
			cumulativeWeight[i] = sum
		#TODO finish random particle selectio
		
	def defineMap(self):
		pass # Define a map based on lines
		
	def getMappedDepth(self):
		pass # Get mapped depth at given position
	
	def onUltrasound(params):
		self.depth = params['distance']

	def noise(self):
		return random.gauss(0.0, 0.5)*0.01

if __name__ == '__main__':
	robot = Robot()
	robot.events.add(EventType.SENSOR_ULTRASOUND, onUltrasound)
	# TODO see if we ca change robot to use a behaviour rather than a behaviour use a robot
