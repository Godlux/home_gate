import os, sys
import json
import time
import hashlib

dirname = os.path.split( sys.argv[0] )[0]
with open( dirname + '/config.json', 'r' ) as registred_devices:
	config = json.load( registred_devices )
	correct_login = config["login"]
	correct_password = config["password"]


def auth_user(login, password):
	# USER AUTH / FILE MODE
	if not check_password_set():   # todo force users to set password
		return False
	if login == correct_login and password == correct_password:
		print("login success")
		return True
	else:
		print("login fail")
		return False


def gen_cookies( request ):
	guest_ip = request.remote_addr
	gen_time = time.time()
	to_hash_str = str(guest_ip)+str(gen_time)
	cookie = hashlib.sha1(to_hash_str.encode('utf-8')).hexdigest()
	save_cookies(cookie)
	return cookie


def save_cookies(cookie):
	current_dirname = os.path.dirname(os.path.realpath(__file__))
	with open( current_dirname + '/cookies.json', 'w' ) as cookies_file:
		json_data = dict()
		json_data["cookie"] = str(cookie)
		json.dump(json_data, cookies_file)


def get_actual_cookies():
	current_dirname = os.path.dirname(os.path.realpath(__file__))
	with open( current_dirname + '/cookies.json', 'r' ) as cookies_file:
		result = json.load(cookies_file)["cookie"]
		return result


def check_auth_token( request_to_check ):
	if not request_to_check.cookies.get( 'auth_token' ):
		return False
	else:
		cookie = request_to_check.cookies.get( 'auth_token' )
		if cookie != get_actual_cookies():
			return False

	return True


def check_password_set():
	if correct_password == "":
		return False
	return True
