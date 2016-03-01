from robot import Robot
from navigateToWaypoint import Navigate
import random
from math import exp, fabs, isinf, cos, sin, radians, atan2, pi
from eventTypes import EventType
from utils import *

class MonteCarloWaypoint(Navigate):

	numParticles = 100

	def __init__(self, robot):
		super(self.__class__, self).__init__(robot)
		
		#init for navigation
		self.step = 0.2
		self.particles = [Particle(0.84, 0.30, 0.0, float(1.0/self.numParticles))]*self.numParticles
		self.depth = float('inf')

		self.x = 0.84
		self.y = 0.30
		self.threshold = 0.03

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

		self.waypoints = [\
			Point(1.8,  0.3), \
			Point(1.8,  0.54), \
			Point(1.38, 0.54), \
			Point(1.38, 1.68), \
			Point(1.14, 1.68), \
			Point(1.14, 0.84), \
			Point(0.84, 0.84), \
			Point(0.84, 0.3)]
		
		# Print map and particles on web
		self.scale = 400
		self.offset = 50
		
		for (a, b) in self.lines:
			print("drawLine:" + str((int(a.x*self.scale) + self.offset, int(a.y*self.scale) + self.offset, int(b.x*self.scale) + self.offset, int(b.y*self.scale) + self.offset)))
		
	
	def run(self):
		running = True
		#while running:
			#print('Enter waypoint coordinate')
			#pointX = input('x:')
			#pointY = input('y:')
		for w in self.waypoints:
			pointX = w.x
			pointY = w.y
			print('Old Position: '+ str(self.x) + ' ' +  str(self.y))
			while((fabs(self.x - pointX) > self.threshold) or (fabs(self.y - pointY) > self.threshold)):
				print('New Position: '+ str(self.x) + ' ' +  str(self.y))
				self.waypoint((pointX, pointY), self.step)
			
			
	def updateAngle(self, a):
		newParticles = []
		for p in self.particles:
			newA = p.a + a + self.noise()
			newA = clampAngle(newA)
			newP = Particle(p.x, p.y, newA, p.p)
			newParticles.append(newP)
		self.particles = newParticles

	def updatePosition(self, d, a):
		self.updateAngle(a)
		# Redo weightings
		self.depth = self.robot.ultraSonic.getValue()
		if isinf(self.depth):
			self.theta = a
			self.x += d*cos(a)
			self.y += d*sin(a)
			return False
		self.particles = [Particle(\
			p.x + (d + self.noise())*cos(p.a), \
			p.y + (d + self.noise())*sin(p.a), \
			p.a, \
			p.p * self.calculate_likelihood(p.x, p.y, p.a, self.depth))\
			for p in self.particles] 
		# Resample high values and cull low values
		self.resample()
		# Get mean of particles
		tX = 0
		tY = 0
		tA = 0
		for p in self.particles:
			tX += p.x*p.p
			tY += p.y*p.p
			tA += p.a*p.p
		#Update the current position
		self.theta = clampAngle(tA)
		#self.theta = a
		self.x = tX
		self.y = tY
		
		# Print particles on web
		print("drawParticles:" + str([(p.x*self.scale + self.offset, p.y*self.scale + self.offset, p.a) for p in self.particles]))
		return True		

	def normalise(self, particles):
		tWeight = sum([p.p for p in particles])
		return [Particle(\
			p.x, p.y, p.a,\
			p.p / tWeight) \
			for p in particles]
		
	def calculate_likelihood(self, x, y, theta, z):
		estimatedDepth = self.getMappedDepth(Point(x, y), theta)
		measuredDepth = z
		variance = 0.02**2	# Error in sonar reading
		K = 1	# Adds robustness, constant  probability for garbage reading
		if not isinf(measuredDepth):
			exponent = fabs(estimatedDepth - measuredDepth)
			return exp((-1*exponent**2)/(2*variance)) + K
		return 1.0
		
	def resample(self):
		#  Normalise particle weightings
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
		
	def intersectLineRay(s, e, p, t):
		det = (sin(t)*(s.x - e.x) - cos(t)*(s.y - e.y))
		if(det == 0):
			return None
		a = (cos(t)*(p.y - s.y) - sin(t)*(p.x - s.x)) / det
		d = ((s.y - e.y)*(p.x - s.x) + (e.x - s.x)*(p.y - s.y)) / det
		if(a < 0.0 or a > 1.0 or d < 0.0):
			return None
		return d
	
	def getMappedDepth(position, angle):
		depth = float('inf')
		for line in lines:
			newDepth = intersectLineRay(line[0], line[1], position, angle)
			print str(line[0]) + ', ' + str(line[1]) + ' = ' + str(newDepth)
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
