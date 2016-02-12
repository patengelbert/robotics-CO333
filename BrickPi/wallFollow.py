from robot import Robot
from eventTypes import EventType
import math

def clamp(value, min, max):
	if(value < min):
		return min
	elif(value > max):
		return max

class WallFollow:
	
	motorBias = 0
	followDistance = 0.2
	speedCoeff = 6

	def __init__(self, robot, events):
		self.robot = robot
		self.events = events

	def start(self):
		self.events.add(EventType.SENSOR_ULTRASOUND, self.onUltrasound)

	def deltaFunction(d):
		return clamp(d, -1, 1)

	def onUltrasound(self, params):
		self.motorBias = deltaFunction(params['distance'] - self.followDistance)
		robot.drive(self.speedCoeff * (1 + self.motorBias)/2, self.speedCoeff * (1 - self.motorBias)/2)

