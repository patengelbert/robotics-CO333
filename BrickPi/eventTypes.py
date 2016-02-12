class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

EventType = Enum(["SENSOR_TOUCH", "SENSOR_ULTRASOUND", "SENSOR_LIGHT", "MOTOR_STOP"])

EventState = Enum(["SENSOR_TOUCH_DOWN", "SENSOR_TOUCH_UP", "SENSOR_ULTRASOUND_DELTA"])

