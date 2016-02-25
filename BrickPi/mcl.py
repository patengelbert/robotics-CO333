from robot import Robot
from navigateToWaypoint import Navigate
from probabilisticMotion import Particle
import random
from math import exp, fabs, isinf, cos, sin, radians, atan2
from eventTypes import EventType

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y


class MonteCarloWaypoint(Navigate):

	numParticles = 100

	def __init__(self, robot):
		super(self.__class__, self).__init__(robot)
		
		#init for navigation
		self.step = 20
		self.particles = [Particle(0, 0, 0, float(1.0/self.numParticles))]*self.numParticles
		self.depth = float('inf')

		#  Define map
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
		running = True
		while running:
			print('Enter waypoint coordinate')
			pointX = input('x:')
			pointY = input('y:')
			
			while self.x != pointX and self.y != pointY:
				self.waypoint((pointX, pointY), self.step)
			
	def updateAngle(self, a):
		self.particles = [Particle(p.x, p.y, p.a+a+self.noise()*180, p.p) for p in self.particles]

	def updatePosition(self, d, a):
		self.updateAngle(a)
		# Redo weightings
		self.depth = self.robot.ultraSonic.getValue()
		self.particles = [Particle(\
			p.x + (d + self.noise())*cos(radians(p.a)), \
			p.y + (d + self.noise())*sin(radians(p.a)), \
			p.a, \
			p.p * self.calculate_likelihood(p.x, p.y, p.a, self.depth))\
			for p in self.particles] 
		# Resample high values and cull low values
		self.resample()
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
			tempX += cos(p.a)*p.p
			tempY += sin(p.a)*p.p
		#Update the current position
		new_A = atan2(tempY,tempX)
		#self.theta = tA
		self.theta = new_A
		self.x = tX
		self.y = tY
		
		# Print particles on web
		print("drawParticles:" + str([(p.x*self.scale + self.offset, p.y*self.scale + self.offset, p.a) for p in self.particles]))

	def normalise(self, particles):
		print [p.p for p in particles]
		tWeight = sum([p.p for p in particles])
		return [Particle(\
			p.x, p.y, p.a,\
			p.p / tWeight) \
			for p in particles]
		
	def calculate_likelihood(self, x, y, theta, z):
		estimatedDepth = self.getMappedDepth(Point(x, y), theta)
		measuredDepth = z
		variance = 0.04	# Error in sonar reading
		K = 0.02	# Adds robustness, constant  probability for garbage reading
		if not isinf(measuredDepth):
			exponent = fabs(estimatedDepth - measuredDepth)
			return exp((-1*exponent**2)/(2*variance)) + K
		return 1.0
		
	def resample(self):
		print [p.p for p in self.particles]
		# Normalise particle weightings
		self.particles = self.normalise(self.particles)
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
		angle = radians(t)
		det = (cos(angle)*(e.y - s.y) - sin(angle)*(e.x - s.x))
		d = (((e.y - s.y)*(s.x - p.y)) - ((e.x - s.x)*(s.y - p.y)))/det
		if(d < 0.0):
			return None
		return d
		
	def getMappedDepth(self, position, angle):
		depth = float('inf')
		for line in self.lines:
			newDepth = self.intersectLineRay(line[0], line[1], position, angle)
			if(newDepth != None and newDepth < depth):
				depth = newDepth
		return depth
	
	def onUltrasound(params):
		self.depth = params['distance']
		print self.depth

	def noise(self):
		return random.gauss(0.0, 0.5)*0.01

if __name__ == '__main__':
	robot = Robot()
	navigate = MonteCarloWaypoint(robot)
	robot.events.add(EventType.SENSOR_ULTRASOUND, navigate.onUltrasound)
	navigate.run()
	# TODO see if we can change robot to use a behaviour rather than a behaviour use a robot
