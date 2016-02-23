from robot import Robot
from navigateToWaypoint import Navigate

class MonteCarloLocation:

	def __init__(self, robot, navigation):
		self.robot = robot
		
		#init for navigation
		self.step = 20
		self.navigation = navigation
	
	def run(self):
		pass

	def updatePoints(self):
		pass # Update MCL points based on movement
		
	def weightPoint(self):
		pass # Weight points based on measured depth vs. mapped depth
		
	def resample(self):
		pass # Split high weighted points, drop low weighted ones
		
	def defineMap(self):
		pass # Define a map based on lines
		
	def getMappedDepth(self):
		pass # Get mapped depth at given position

