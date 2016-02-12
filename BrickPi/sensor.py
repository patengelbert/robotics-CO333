import brickpi
from eventTypes import EventType, EventState

"""
Base class for sensors, enabling it on the given port
"""
class Sensor(object):
	
	def __init__(self, interface, port, events, sensorType):
		self.interface = interface
		self.port = port
		self.events = events
		self.sensorType = sensorType
		interface.sensorEnable(port, self.sensorType)

	def check(self):
		raise NotImplementedError()

"""
A single touch sensor
"""
class PushSensor(Sensor):

	def __init__(self, position, *args, **kwargs):
		self.position = position
		super(PushSensor, self).__init__(*args, **kwargs)
		self.state = False

	def check(self):
		cvalue = bool(self.interface.getSensorValue(self.port)[0])
		if cvalue != self.state:
			self.state = cvalue
			self.events.invoke(EventType.SENSOR_TOUCH, {'position': self.position, 'down': cvalue})

	def getState(self):
		return self.state

"""
Single ultrasonic sensor
"""
class UltraSonicSensor(Sensor):
	def __init__(self, *args, **kwargs):
		super(UltraSonicSensor, self).__init__(*args, **kwargs)
		self.value = 0

	def check(self):
		ivalue = self.interface.getSensorValue(self.port)[0]
		if(self.value != ivalue):
			self.value = ivalue
			cvalue = float('inf')
			if(ivalue < 255):
				cvalue = (ivalue - 7)/100.0
			self.events.invoke(EventType.SENSOR_ULTRASOUND, {'distance':cvalue})

"""
Implements the 'either' and 'both' positions for two touch sensors
"""
class Bumper:

	leftDown = False
	rightDown = False

	def bumperEvent(params):
		wasBoth = leftDown & rightDown
		wasEither = leftDown | rightDown
		if(params['position'] == 'left'):
			leftDown = params['down']
		if(params['position'] == 'right'):
			rightDown = params['down']
		isBoth = leftDown & rightDown
		isEither = leftDown | rightDown
		if(isBoth != wasBoth):
			self.events.invoke(EventType.SENSOR_TOUCH, {'position':'both', 'down':isBoth})
		if(isEither != wasEither):
			self.events.invoke(EventType.SENSOR_TOUCH, {'position':'either', 'down':isEither})

	def __init__(self, events):
		self.events = events
		events.add(EventType.SENSOR_TOUCH, self.bumperEvent)

