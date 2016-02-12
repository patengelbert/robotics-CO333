import brickpi
from eventTypes import EventType, EventState

class Sensor(object):
	
	def __init__(self, interface, port, events, sensorType):
		self.interface = interface
		self.port = port
		self.events = events
		self.sensorType = sensorType
		interface.sensorEnable(port, self.sensorType)

	def check(self):
		raise NotImplementedError()

class PushSensor(Sensor):

	def __init__(self, position, *args, **kwargs):
		self.position = position
		self.eventType = EventType.SENSOR_TOUCH
		super(PushSensor, self).__init__(*args, **kwargs)
		self.state = EventState.SENSOR_TOUCH_UP

	def check(self):
		cvalue = EventState.SENSOR_TOUCH_DOWN if self.interface.getSensorValue(self.port)[0] else EventState.SENSOR_TOUCH_UP
		if cvalue != self.state:
			self.state = cvalue
			self.events.invoke(EventType.SENSOR_TOUCH, {'position': self.position, 'state': cvalue})

	def getState(self):
		return self.state

class UltraSonicSensor(Sensor):

	def __init__(self, *args, **kwargs)
		self.eventType = EventType.SENSOR_TOUCH
		super(UltraSonicSensor, self).__init__(*args, **kwargs)
		
	
	
		
			
		
