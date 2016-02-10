from enum import Enum

def EventTypes(Enum):
	SENSOR_TOUCH = 100
	SENSOR_ULTRASOUND = 101
	SENSOR_LIGHT = 102

	WHEEL_POSITION_REACHED = 200

# All values above 1000 are reserved for states
def EventStates(Enum):
	SENSOR_TOUCH_DOWN = 1000
	SENSOR_TOUCH_UP = 1001
