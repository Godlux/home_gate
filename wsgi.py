from flask import Flask
from flask import request, send_from_directory
from flask import render_template
from flask import make_response
from api.absctarct_devices import PowerableDevice, ReadableDevice
from api_handler import ApiHandler

app = Flask(__name__, template_folder='static/html/')


# Active Routes
@app.route('/')
def show_main_page():
	if not check_auth_token( request_to_check=request ):
		return show_login_page()

	str_response = ""
	for device in api_handler.get_all_devices():
		str_response += device.name + ", \n"
	print(str_response)

	return render_template('main_page.html', devices=api_handler.get_all_devices() )


@app.context_processor
def object_check_type_util():
	def get_type(object):
		if isinstance(object, PowerableDevice):
			return "powerable"
		if isinstance( object, ReadableDevice ):
			return "readable"
		return "undefined"
	return dict(get_type=get_type)


@app.route('/login')
def show_login_page():
	if check_auth_token( request_to_check=request ):
		return show_main_page()

	return send_from_directory('static/html/', "login_page.html")


# Flask WSGI API
@app.route('/do_login', methods=['GET', 'POST'])
def do_login():
	data = request.json

	from dynamic.login_handler import auth_user
	auth_result = auth_user(data["login"], data["password"])
	response = make_response("true" if auth_result else "false")

	if auth_result:
		response.set_cookie( "auth_token", "true", max_age=60 * 60 * 24 * 30 )

	return response


@app.route('/do_logout')
def do_logout():
	if not check_auth_token( request_to_check=request ):
		return show_login_page()

	response = make_response("true")
	response.set_cookie( "auth_token", "true", max_age=60 * 60 * 24 * 30 )

	return response


@app.route('/api', methods=['GET', 'POST'])
def send_to_api_handler():
	if not check_auth_token( request_to_check=request ):
		return "false"

	data = request.json
	return "true" if api_handler.handle(device_id=data["device"], action=data["action"]) else "false" # todo


@app.route('/get_devices_info', methods=['GET', 'POST'])
def return_device_info():
	if not check_auth_token( request_to_check=request ):
		return "false"

	data = request.json
	devices_info = api_handler.get_devices_info()
	return devices_info


def check_auth_token( request_to_check ):
	if not request_to_check.cookies.get( 'auth_token' ):
		return False
	else:
		cookie = request_to_check.cookies.get( 'auth_token' )
		if cookie != "true":
			return False

	return True


# Static files
@app.route('/favicon.ico')
def send_favicon():
	return send_from_directory('static/ico/', "favicon.ico")


@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('static/js', path)


@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('static/css', path)


if __name__ == '__main__':
	print( "Initializing Devices..." )
	api_handler = ApiHandler()
	print( "Devices Initialized." )
	app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)