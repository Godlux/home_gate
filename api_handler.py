from api.absctarct_devices import PowerableDevice, ReadableDevice
from api.mFi.mFiApi import MfiApi
import threading
import time
mfi_api = MfiApi()


class ApiHandler( threading.Thread ):
	""" Общий обработчик событий, связанных с различными API """
	devices = list()
	devices_map = dict()

	def __init__( self ):
		super().__init__()
		self.device_info_json = dict()

		# Init and register mFid devices
		for device in mfi_api.get_devices():
			self.devices_map[str(device.id)] = device
			self.devices.append(device)

	def run(self):
		while True:
			print("updating devices info...")
			try:
				self.update_devices_info()
			except ConnectionError:
				print("updating ends with fail, device not respond")
			time.sleep(2)

	def get_all_devices( self ):
		return self.devices

	def update_devices_info( self ):
		devices = self.devices
		devices_info = dict()
		for device in devices:
			if isinstance(device, PowerableDevice):
				devices_info[str(device.id)] = "On" if device.get_power_state() else "Off"
			if isinstance(device, ReadableDevice):
				devices_info[str(device.id)] = str(device.get_sensor_info())
		import json
		print( f"updated to {self.device_info_json}" )
		self.device_info_json = json.dumps(devices_info)

	def get_devices_info( self ):
		return self.device_info_json

	def get_device_with_id(self, device_id):
		try:
			return self.devices_map[str(device_id)]
		except KeyError:
			raise Exception("No device with selected id Found.")

	def handle(self, device_id, action):
		print(f"device_id: {device_id}, action: {action}")
		device = self.get_device_with_id(device_id)
		if action == "power_toggle":
			return self.power_toggle(device)
		if action == "turn_off":
			return self.turn_off(device)
		if action == "turn_on":
			return self.turn_on(device)
		return False

	@staticmethod
	def power_toggle( device ):
		if not isinstance(device, PowerableDevice):
			raise Exception("This device can't toggle it's power!")
		if device.get_power_state():
			device.turn_off_device()
			return True
		else:
			device.turn_on_device()
			return True

	@staticmethod
	def turn_on( device ):
		if not isinstance(device, PowerableDevice):
			raise Exception("This device can't toggle it's power!")
		device.turn_on_device()

	@staticmethod
	def turn_off( device ):
		if not isinstance(device, PowerableDevice):
			raise Exception("This device can't toggle it's power!")
		device.turn_off_device()
