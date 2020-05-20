from api.abstract_api import ApiBase
from .devices import Device, MPowerDevice, MPortDevice
from .mfi_device_listener import MfiListener
import os
import sys


class MfiApi( ApiBase ):
	""" The base class for api """

	def __init__(self):
		self.mfi_device_listener = MfiListener()
		self.mfi_device_listener.start()

	def get_devices(self):
		import json
		mfi_devices = list()

		# AUTO-SEARCH MODE
		# devices_dict = self.mfi_device_listener.devices
		#
		# with open ('devices.json', 'r') as registred_devices:
		# 	 json.load(registred_devices)
		#
		# 	 print(len(devices_dict))  # fixme debug
		# 	 for device_ip in devices_dict:
		# 		 data = devices_dict[device_ip]
		# 		 print(f"D{device_ip}, DA{data}")
		# 		 for registred_device in registred_devices:
		# 			 if device_ip == registred_device["ip"]:
		# 				 device = Device(name=registred_device["name"], ip=device_ip, mfi_data=data)
		# 				 devices.append(device)

		# FILE MODE
		dirname = os.path.split( sys.argv[0] )[0]
		with open(dirname+'/devices.json', 'r') as registred_devices:
			loaded_devices = json.load( registred_devices )

			for device in loaded_devices:
				# if device associated with other api - skipping
				if device["api"] != "mFi":
					continue
				if device["device"] == "mPort":
					mfi_devices.append( MPortDevice( name=device["name"], device_id=device["id"], ip=device["ip"], mfi_data="", sensor_id=device["port"] ) )
				if device["device"] == "mPower":
					mfi_devices.append( MPowerDevice(name=device["name"], device_id=device["id"], ip=device["ip"],  mfi_data="") )

			# preparing to next work
			# import threading
			for device in mfi_devices:
				# thread = threading.Thread(target=device.do_login(), daemon=True)
				# thread.start()
				device.do_login()

		return mfi_devices

	def get_commands_for_device(self, device_id):
		return str()

	def turn_on_device(self, device_id):
		pass

	def turn_off_device(self, device_id):
		pass

	def send_command_to_device(self, device_id):
		pass