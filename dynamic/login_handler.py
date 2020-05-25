import os, sys
import json

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

def gen_coockie


def check_password_set():
	if correct_password == "":
		return False
	return True