from abc import ABCMeta, abstractmethod, abstractproperty


class Device( object ):
	""" base device class"""
	def __init__(self, name, device_id, ip):
		self.name = name
		self.id = device_id
		self.ip = ip


class PowerableDevice( object ):
	""" Interface for devices, that can be powered on """

	@abstractmethod
	def turn_on_device(self):
		return False

	@abstractmethod
	def turn_off_device(self):
		return False

	@abstractmethod
	def get_power_state(self):
		return False


class ReadableDevice( object ):
	""" Sensor interface """

	@abstractmethod
	def get_sensor_info(self, id):
		return False
