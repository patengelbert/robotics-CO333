from robot import Robot

class MonteCarloLocation:

	def __init__(self, robot):
		self.robot = robot
	
	def run(self):
		pass

	def updatePoints(self):
		pass # Update MCL points based on movement
		
	def weightPoints(self):
		pass # Weight points based on measured depth vs. mapped depth
		
	def cullPoints(self):
		pass # Split high weighted points, drop low weighted ones
		
	def defineMap(self):
		pass # Define a map based on lines
		
	def getMappedDepth(self):
		pass # Get mapped depth at given position

