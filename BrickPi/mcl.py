from robot import Robot
from navigateToWaypoint import Navigate

class MonteCarloWaypoint(Navigate):
	
	numParticles = 100

	def __init__(self, robot):
		super(Navigate).__init__(self, robot)
		
		#init for navigation
		self.step = 20
		self.particles = [Particle(0, 0, 0, 1/sel.numParticles)]*self.numParticles
	
	def run(self):
		running = true
		while running:
			print('Enter waypoint coordinate')
			pointX = input('x:')
			pointY = input('y:')
			
			while self.x != pointX and self.y != pointY
				self.waypoint((pointX, pointY), self.step)
				updatePoints()
			

	def updatePoints(self, d, a):
		# Redo weightings
		self.particles = [Particle(\
			p.x + (d + self.noise())*cos(p, a), \
			p.y + (d + self.noise())*sin(p, a), \
			p.a + self.noise() + a, \
			p.p * calculate_likelihood(p.x, p.y, p.a, self.depth))\
			for p in self.particles] 
		# Resample high values and cull low values
		self.particles = resample(self.particles)
		# Normalise Weightings
		self.particles = normalise(self.particles)
		tX = 0, tY = 0, tA = 0
		for p in self.particles:
			tX += p.x
			tY += p.y
			tA += p.a
		self.updatePosition(tA/self.numParticles, \
			tX/self.numParticles, \
			tY/self.numParticles)


	def normalise(self, particles):
		tWeight = 0
		(tWeight += p.p) for p in particles
		return [Particle(\
			p.x, p.y, p.a,\
			p.p / tWeight) \
			for p in particles]
		
	def weightPoint(self, point):
		pass # Weight points based on measured depth vs. mapped depth
		
	def resample(self):
		pass # Split high weighted points, drop low weighted ones
		
	def defineMap(self):
		pass # Define a map based on lines
		
	def getMappedDepth(self):
		pass # Get mapped depth at given position

	def noise(self):
		return random.gauss(0.0, 0.5)*0.01

if __name__ == '__main__':
	robot = Robot()
	# TODO see if we ca change robot to use a behaviour rather than a behaviour use a robot
