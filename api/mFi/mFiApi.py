from api.abstract_api import ApiBase
from .devices import Device, MPowerDevice, MPortDevice
from .mfi_device_listener import MfiListener
import os
import sys
import time


class MfiApi( ApiBase ):
	""" The base class for api """

	def __init__(self):
		self.mfi_device_listener = MfiListener()
		self.mfi_device_listener.start()

	def get_devices(self):
		import json
		mfi_devices = list()

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

			# AUTO-SEARCH IP BY MAC
			time.sleep( 30 )  # fixme: hack - waiting to search new devices
			devices_by_mac_dict = self.mfi_device_listener.devices

			for device in loaded_devices:
				# if device associated with other api - skipping
				if device["api"] != "mFi":
					continue

				mfi_data = ""
				# Trying to find device by mac-address, if can't - use ip in config
				try:
					ip = devices_by_mac_dict[device["mac"]][0]
				except KeyError:
					try:
						ip = devices_by_mac_dict[device["wifi_mac"]][0]
					except KeyError:
						print( f"Using config ip for device with mac [{device['mac']}] not found in devices list: {devices_by_mac_dict.keys()}" )
						ip = device["ip"]

				if device["device"] == "mPort":
					mfi_devices.append( MPortDevice( name=device["name"], device_id=device["id"], ip=ip, login=device["login"], password=device["password"], mfi_data=mfi_data, self_json=device, sensor_id=device["port"] ) )
				if device["device"] == "mPower":
					mfi_devices.append( MPowerDevice(name=device["name"], device_id=device["id"], ip=ip, login=device["login"], password=device["password"], mfi_data=mfi_data, self_json=device) )

			self.mfi_device_listener.stop()

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