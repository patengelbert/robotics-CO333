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
		self.eventType = EventType.SENSOR_TOUCH
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

	def __init__(self, *args, **kwargs)
		self.eventType = EventType.SENSOR_TOUCH
		super(UltraSonicSensor, self).__init__(*args, **kwargs)

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
			rightDown = parans['down']
		isBoth = leftDown & rightDown
		isEither = leftDown | rightDown
		if(isBoth != wasBoth):
			self.events.invoke(EventType.SENSOR_TOUCH, {'position':'both', 'down':isBoth)
		if(isEither != wasEither)
			self.events.invoke(EventType.SENSOR_TOUCH, {'position':'either', 'down':isEither)

	def __init__(self, events):
		self.events = events
		events.add(SENSOR_TOUCH, bumperEvent)		
