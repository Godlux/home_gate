from ..absctarct_devices import Device, PowerableDevice, ReadableDevice
import threading
import requests
import time
import json


class MFiDevice( Device ):
	""" Mfi base device class"""
	def __init__(self, name, device_id, ip, mfi_data):
		super().__init__( name=name, device_id=device_id, ip=ip )
		self.mfi_data = mfi_data


class MPowerDevice( MFiDevice, PowerableDevice ):

	def __init__(self, name, device_id, ip, mfi_data, login="admin", password="password", use_https=False, verify_ssl=True):
		super().__init__(name, device_id, ip, mfi_data)

		# settings
		self.login = login
		self.password = password
		self.use_https = use_https    #fixme: use config
		self.verify_ssl = verify_ssl

		# do not touch
		self._http_prefix = "https" if self.use_https else "http"
		self._wsgi_url = f"{self._http_prefix}://{self.ip}"
		self._headers = None
		self.sensor_id = 1     # correct id for MPowerDevice

	def do_login(self):
		"""
		## login
		# example: curl -X POST -d "username=admin&password=password" -b "AIROS_SESSIONID=012345678901" -k https://192.168.1.45/login.cgi
		"""

		# Get cookies
		self._rsession = requests.Session()
		response = self._rsession.get(f"{self._wsgi_url}/login.cgi", verify=self.verify_ssl)
		# Set cookies
		auth_cookies = self._rsession.cookies['AIROS_SESSIONID']
		self._headers =  {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
		'AIROS_SESSIONID': auth_cookies,
		}
		open("login_response.html", 'w').write(response.text)
		open("cookies_log.txt", 'a').write(auth_cookies + "\n")
		# Login with cookies
		response = self._rsession.post(f"{self._wsgi_url}/login.cgi", data={'username': self.login, 'password': self.password}, headers=self._headers, verify=self.verify_ssl)
		open("afterlogin_response.html", 'w').write(response.text)

		return response

	def verify_login(self):
		if self._headers is None:
			return False
		return True

	@staticmethod
	def response_contains_login_page( response ):
		if "Login" in response.text:
			return True
		return False

	def turn_on_device(self):
		## turn on device
		# example: curl -X PUT -d "resource=1&output=1&dimmer_level=50" -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/sensors/1/
		response = self._rsession.put(f"{self._wsgi_url}/sensors/{self.sensor_id}/", data={'output': 1, }, headers=self._headers, verify=self.verify_ssl)
		if self.response_contains_login_page( response ):
			self.do_login()
			return self.turn_on_device()
			# open("turnOn_response.html", 'w').write(response.text)
		print(f"DEBUG: TURNING ON : {response}")  # fixme: remove me
		return response

	def turn_off_device(self):
		## turn off device
		# example: curl -X PUT -d "resource=1&output=1&dimmer_level=50" -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/sensors/1/
		response = self._rsession.put(f"{self._wsgi_url}/sensors/{self.sensor_id}/", data={'output': 0, }, headers=self._headers, verify=self.verify_ssl)
		if self.response_contains_login_page( response ):
			self.do_login()
			return self.turn_off_device()
			# open("turnOff_response.html", 'w').write(response.text)
		print(f"DEBUG: TURNING OFF : {response}")  # fixme: remove me
		return response

	def get_power_state(self):
		## turn off device
		# example: curl -X PUT -d "resource=1&output=1&dimmer_level=50" -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/sensors/1/
		response = self._rsession.get(f"{self._wsgi_url}/sensors/{self.sensor_id}/", headers=self._headers, verify=self.verify_ssl)
		if self.response_contains_login_page( response ):
			self.do_login()
			return self.get_power_state()
		data = response.json()
		is_enabled = True if data["sensors"][0]["output"] == 1 else False
		print(f'DEBUG: DEVICE ENABLED? : {is_enabled}')  # fixme: remove me
		return is_enabled

	def go_to_power_page(self, id):
		## go to power page
		if not self.verify_login():
			self.do_login()
		response = self._rsession.get(f"{self._wsgi_url}/sensors/{id}/", headers=self._headers, verify=self.verify_ssl)
		open("powerpage_response.html", 'w').write(response.text)
		return response

	def do_logout(self):
		## logout
		# example: curl -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/logout.cgi
		if not self.verify_login():
			return True
		response = self._rsession.get(f"{self._wsgi_url}/logout.cgi", headers=self._headers, verify=self.verify_ssl)
		open("afterlogout_response.html", 'w').write(response.text)
		return response


class MPortDevice( MFiDevice, ReadableDevice ):

	def __init__(self, name, device_id, ip, mfi_data, sensor_id, login="admin", password="password", use_https=False, verify_ssl=True):
		super().__init__(name, device_id, ip, mfi_data)

		# settings
		self.login = login
		self.password = password
		self.use_https = use_https    #fixme: use config
		self.verify_ssl = verify_ssl

		# do not touch
		self._http_prefix = "https" if self.use_https else "http"
		self._wsgi_url = f"{self._http_prefix}://{self.ip}"
		self._headers = None
		self.sensor_id = sensor_id       # specified by 'port' in json config

	def do_login(self):
		## login
		# example: curl -X POST -d "username=admin&password=password" -b "AIROS_SESSIONID=012345678901" -k https://192.168.1.45/login.cgi
		# get cookies
		self._rsession = requests.Session()
		response = self._rsession.get(f"{self._wsgi_url}/login.cgi", verify=self.verify_ssl)
		# set cookies
		auth_cookies = self._rsession.cookies['AIROS_SESSIONID']
		self._headers =  {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
		'AIROS_SESSIONID': auth_cookies,
		}
		open("login_response.html", 'w').write(response.text)
		open("cookies_log.txt", 'a').write(auth_cookies + "\n")

		## login with cookies
		response = self._rsession.post(f"{self._wsgi_url}/login.cgi", data={'username': self.login, 'password': self.password}, headers=self._headers, verify=self.verify_ssl)
		open("afterlogin_response.html", 'w').write(response.text)
		return response

	def verify_login(self):
		if self._headers is None:
			return False
		return True

	@staticmethod
	def response_contains_login_page( response ):
		if "Login" in response.text:
			return True
		return False

	def get_sensor_info(self):
		## turn off device
		# example: curl -X PUT -d "resource=1&output=1&dimmer_level=50" -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/sensors/1/
		self.verify_login()
		response = self._rsession.get(f"{self._wsgi_url}/sensors/{self.sensor_id}/", headers=self._headers, verify=self.verify_ssl)
		if self.response_contains_login_page( response ):
			self.do_login()
			return self.get_sensor_info()
			# open("mPower_sensorInfo_response.html", 'w').write(response.text)
		data = response.json()
		info = "motion" if data["sensors"][0]["input1"] == 1 else "no motion"
		return info

	def get_sensors_info(self):
		## turn off device
		# example: curl -X PUT -d "resource=1&output=1&dimmer_level=50" -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/sensors/1/
		self.verify_login()
		response = self._rsession.get(f"{self._wsgi_url}/sensors/", headers=self._headers, verify=self.verify_ssl)
		if self.response_contains_login_page( response ):
			self.do_login()
			return self.get_sensors_info()
			# open("mPower_allSensorsInfo_response.html", 'w').write(response.text)
		return response

	def do_logout(self):
		## logout
		# example: curl -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/logout.cgi
		self.verify_login()
		response = self._rsession.get(f"{self._wsgi_url}/logout.cgi", headers=self._headers, verify=self.verify_ssl)
		if self.response_contains_login_page( response ):
			return True
			# open("afterlogout_response.html", 'w').write(response.text)
		return True
