from robot import Robot
from eventTypes import EventType
import math

def clamp(value, max):
	if(value < -max):
		return -max
	elif(value > max):
		return max
	return value

class WallFollow:
	
	motorBias = 0
	followDistance = 0.1
	speedCoeff = 6

	def __init__(self, robot, events):
		self.robot = robot
		self.events = events

	def start(self):
		self.events.add(EventType.SENSOR_ULTRASOUND, self.onUltrasound)

	def deltaFunction(self, d):
		return clamp(d*5, 0.6)

	def onUltrasound(self, params):
		self.motorBias = self.deltaFunction(params['distance'] - self.followDistance)
		print self.motorBias
		robot.drive(self.speedCoeff * (1 - self.motorBias)/2, self.speedCoeff * (1 + self.motorBias)/2)

if __name__ == '__main__':
	robot = Robot()
	robot.setPID(150, 0, 0)
	wallFollow = WallFollow(robot, robot.events)
	wallFollow.start()
	robot.mainLoop()

