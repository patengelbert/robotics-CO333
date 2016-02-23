from robot import Robot
from navigateToWaypoint import Navigate

class MonteCarloWaypoint(Navigate):

	def __init__(self, robot):
		self.robot = robot
		
		#init for navigation
		self.step = 20
		self.particles = [Particle(0, 0, 0)]*self.numParticles
	
	def run(self):
		running = true
		while running:
			print('Enter waypoint coordinate')
			pointX = input('x:')
			pointY = input('y:')
			
			while self.x != pointX and self.y != pointY
				self.waypoint((pointX, pointY), self.step)
				updatePoints()
			

	def updatePoints(self):
		#self.particles = [Particle{\
		#	p.x + (d + self.noise())*cos(p, a), \
		#	p.y + (d + 
		pass
		
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
