from enum import Enum

#def EventTypes():
#	SENSOR_TOUCH = 100
#	SENSOR_ULTRASOUND = 101
#	SENSOR_LIGHT = 102

#	WHEEL_POSITION_REACHED = 200

# All values above 1000 are reserved for states
#def EventStates():
#	SENSOR_TOUCH_DOWN = 1000
#	SENSOR_TOUCH_UP = 1001

EventTypes = Enum(["SENSOR_TOUCH", "SENSOR_ULTRASOUND", "SENSOR_LIGHT"])

EventStates = Enum(["SENSOR_TOUCH_DOWN", "SENSOR_TOUCH_UP"])
