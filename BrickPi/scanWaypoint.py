import brickpi
from robot import Robot
from navigateToWaypoint import Navigate
from place_rec_bits import PlaceRecognition
from math import radians
from utils import *

class ScanWaypoint(Navigate):
	
	def __init__(self, robot):
		super(self.__class__, self).__init__(robot)
		
		self.waypoints = [ \
			Point(0.84, 0.30), \
			Point(1.80, 0.30), \
			Point(1.80, 0.54), \
			Point(1.38, 0.54), \
			Point(1.38, 1.68)  \
		]
		self.idx = 0
		self.p = PlaceRecognition(robot)
		
		
	def recognize(self):
		# Identify the waypoint we're currently at
		result = self.p.recognize_location()
		self.idx = result['location']
		wp = self.waypoints[self.idx]
		self.x = wp.x
		self.y = wp.y
		self.a = radians(result['angle'])
	
	def run(self):
		self.recognize()
		for i in range(len(self.waypoints)):
			if(self.idx >= len(self.waypoints)):
				self.idx = 0
			self.waypoint(self.waypoints[idx])
			# Beep
			print '\a'
			self.idx += 1

if __name__ == '__main__':
	robot = Robot()
	b = ScanWaypoint(robot)
	b.run()

