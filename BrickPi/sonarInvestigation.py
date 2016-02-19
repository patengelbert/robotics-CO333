from robot import Robot
from eventTypes import EventType

"""
calibrate the sonar by comparing the values it returns with ground truth obtained from measurements
with a ruler or tape measure.
"""
def onUltrasound(params):
	print("Distance:" + str(params['distance']))

if __name__ == '__main__':
	robot = Robot()
	robot.events.add(EventType.SENSOR_ULTRASOUND, onUltrasound)
	robot.mainLoop()

