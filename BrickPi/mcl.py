from robot import Robot
from navigateToWaypoint import Navigate
from probabilisticMotion import Particle
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

		# Define map
		self.lines = [\
			(Point(0.00, 0.00), Point(0.00, 1.68)), \
			(Point(0.00, 1.68), Point(0.84, 1.68)), \
			(Point(0.84, 1.26), Point(0.84, 2.10)), \
			(Point(0.84, 2.10), Point(1.68, 2.10)), \
			(Point(1.68, 2.10), Point(1.68, 0.84)), \
			(Point(1.68, 0.84), Point(2.10, 0.84)), \
			(Point(2.10, 0.84), Point(2.10, 0.00)), \
			(Point(2.10, 0.00), Point(0.00, 0.00))  \
		]
		
		# Print map and particles on web
		self.scale = 400
		self.offset = 100
		
		for (a, b) in self.lines:
			print("drawLine:" + str((int(a.x*self.scale) + self.offset, int(a.y*self.scale) + self.offset, int(b.x*self.scale) + self.offset, int(b.y*self.scale) + self.offset)))
		
	
	def run(self):
		running = true
		while running:
			print('Enter waypoint coordinate')
			pointX = input('x:')
			pointY = input('y:')
			
			while self.x != pointX and self.y != pointY:
				self.waypoint((pointX, pointY), self.step)
			

	def updatePosition(self, d, a):
		# Redo weightings
		self.particles = [Particle(\
			p.x + (d + self.noise())*cos(p.a), \
			p.y + (d + self.noise())*sin(p.a), \
			p.a + self.noise() + a, \
			p.p * calculate_likelihood(p.x, p.y, p.a, self.depth))\
			for p in self.particles] 
		# Resample high values and cull low values
		resample()
		# Get mean of particles
		tX = 0
		tY = 0
		tA = 0
		tempX = 0
		tempY = 0
		for p in self.particles:
			tX += p.x*p.p
			tY += p.y*p.p
			#tA += p.a*p.p
			tempX += math.cos(p.a)*p.p
			tempY += math.sin(p.a)*p.p
		#Update the current position
		new_A = math.atan2(tempY,tempX)
		#self.theta = tA
		self.theta = new_A
		self.x = tX
		self.y = tY
		
		# Print particles on web
		print("drawParticles:" + str([(p.x*self.scale + self.offset, p.y*self.scale + self.offset, p.a) for p in self.particles]))

	def normalise(self, particles):
		tWeight = sum([p.p for p in particles])
		return [Particle(\
			p.x, p.y, p.a,\
			p.p / tWeight) \
			for p in particles]
		
	def calculate_likelihood(self, x, y, theta, z):
		estimateDepth = getMappedDepth()
		measuredDepth = z
		variance = 0.04	# Error in sonar reading
		K = 0.02	# Adds robustness, constant  probability for garbage reading
		if not isinf(measuredDepth):
			exponent = fabs(estimatedDepth - measuredDepth)
			return exp((-1*exponent**2)/(2*variance)) + K
		return 1.0
		
	def resample(self):
		# Normalise particle weightings
		self.particles = normalise(self.particles)
		# New particle set
		newParticles = [Particle(0, 0, 0)]*self.numParticles
		
		# Generate cumulative weight array
		cumulativeWeight = [0]*self.numParticles
		cumulativeWeight[0] = self.particles[0].p
		for i, tempParticle in list(enumerate(self.particles))[1:]:
			cumulativeWeight[i] = cumulativeWeight[i-1] + tempParticle.p
		
		# Pick new particles for the set
		for i in range(0,self.numParticles):
			rndNum = random.random()
			for j,weight in enumerate(cumulativeWeight):
				if rndNum <= weight:
					newParticles[i] = self.particles[j]
					break
		self.particles = newParticles
		self.normalise(self.particles)
		
	def intersectLineRay(self, s, e, p, t):
		det = (cos(t)*(s.x - e.x) - sin(t)*(s.y - e.y))
		a = (sin(t)*(p.y - s.y) - cos(t)*(p.x - s.x)) / det
		d = ((s.y - e.y)*(p.x - s.x) + (e.x - s.x)*(p.y - s.y)) / det
		if(a < 0.0 or a > 1.0 or d < 0.0):
			return None
		return d
		
	def getMappedDepth(self, position, angle):
		depth = float('inf')
		for line in self.lines:
			newDepth = self.lineRayIntersect(line[0], line[1], position, angle)
			if(newDepth != None and newDepth < depth):
				depth = newDepth
		return depth
	
	def onUltrasound(params):
		self.depth = params['distance']

	def noise(self):
		return random.gauss(0.0, 0.5)*0.01

if __name__ == '__main__':
	robot = Robot()
	navigate = MonteCarloNavigate(robot)
	robot.events.add(EventType.SENSOR_ULTRASOUND, navigate.onUltrasound)
	navigae.run()
	# TODO see if we can change robot to use a behaviour rather than a behaviour use a robot
