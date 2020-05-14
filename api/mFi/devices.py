import threading
import requests
import time
import json


class Device( object ):
	""" Mfi base device class"""
	def __init__(self, name, ip, mfi_data):
		self.name = name
		self.ip = ip
		self.mfi_data = mfi_data


class MFiDevice( Device ):

	def __init__(self, name, ip, mfi_data, login="admin", password="password", use_https=False, verify_ssl=True):
		super().__init__(name, ip, mfi_data)

		# settings
		self.login = login
		self.password = password      #fixme: use config
		self.use_https = use_https    #fixme: use config
		self.verify_ssl = verify_ssl

		# do not touch
		self._http_prefix = "https" if self.use_https else "http"
		self._wsgi_url = f"{self._http_prefix}://{self.ip}"
		self._headers = None

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
			input("Login incorrect, press Enter to continue")
			raise Exception("_headers is None!")
		return True

	def turn_on_device(self, id):
		## turn on device
		# example: curl -X PUT -d "resource=1&output=1&dimmer_level=50" -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/sensors/1/
		self.verify_login()
		response = self._rsession.put(f"{self._wsgi_url}/sensors/{id}/", data={'output': 1, }, headers=self._headers, verify=self.verify_ssl)
		open("turnOn_response.html", 'w').write(response.text)
		return response

	def turn_off_device(self, id):
		## turn off device
		# example: curl -X PUT -d "resource=1&output=1&dimmer_level=50" -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/sensors/1/
		self.verify_login()
		response = self._rsession.put(f"{self._wsgi_url}/sensors/{id}/", data={'output': 0, }, headers=self._headers, verify=self.verify_ssl)
		open("turnOff_response.html", 'w').write(response.text)
		return response

	def get_device_info(self, id):
		## turn off device
		# example: curl -X PUT -d "resource=1&output=1&dimmer_level=50" -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/sensors/1/
		self.verify_login()
		response = self._rsession.get(f"{self._wsgi_url}/sensors/{id}/", headers=self._headers, verify=self.verify_ssl)
		open("deviceInfo_response.html", 'w').write(response.text)
		return response

	def go_to_power_page(self, id):
		## go to power page
		self.verify_login()
		response = self._rsession.get(f"{self._wsgi_url}/sensors/{id}/", headers=self._headers, verify=self.verify_ssl)
		open("powerpage_response.html", 'w').write(response.text)
		return response

	def do_logout(self):
		## logout
		# example: curl -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/logout.cgi
		self.verify_login()
		response = self._rsession.get(f"{self._wsgi_url}/logout.cgi", headers=self._headers, verify=self.verify_ssl)
		open("afterlogout_response.html", 'w').write(response.text)
		return response


class MPrortDevice( Device ):

	def __init__(self, name, ip, mfi_data):
		super().__init__(name, ip, mfi_data)

		# settings
		self.ip = "192.168.1.51"
		self.use_https = False
		self.verify_ssl = True
		self.login = "admin"
		self.password = "password"

		# do not touch
		self._http_prefix = "https" if self.use_https else "http"
		self._wsgi_url = f"{self._http_prefix}://{self.ip}"
		self._headers = None

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
			input("Login incorrect, press Enter to continue")
			raise Exception("_headers is None!")
		return True

	def get_sensor_info(self, id):
		## turn off device
		# example: curl -X PUT -d "resource=1&output=1&dimmer_level=50" -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/sensors/1/
		self.verify_login()
		response = self._rsession.get(f"{self._wsgi_url}/sensors/{id}/", headers=self._headers, verify=self.verify_ssl)
		open("mPower_sensorInfo_response.html", 'w').write(response.text)
		return response

	def get_sensors_info(self):
		## turn off device
		# example: curl -X PUT -d "resource=1&output=1&dimmer_level=50" -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/sensors/1/
		self.verify_login()
		response = self._rsession.get(f"{self._wsgi_url}/sensors/", headers=self._headers, verify=self.verify_ssl)
		open("mPower_allSensorsInfo_response.html", 'w').write(response.text)
		return response

	def do_logout(self):
		## logout
		# example: curl -b "AIROS_SESSIONID=012345678901012345678901012345678901" 192.168.1.45/logout.cgi
		self.verify_login()
		response = self._rsession.get(f"{self._wsgi_url}/logout.cgi", headers=self._headers, verify=self.verify_ssl)
		open("afterlogout_response.html", 'w').write(response.text)
		return response
