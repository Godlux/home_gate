from flask import Flask
from flask import request, send_from_directory
import api_handler  #TODO move all api into api_handler

app = Flask(__name__)


# Active Routes
@app.route('/')
def show_main_page():
    send_from_directory('static/html/', "main_page.html")
    str_response = ""
    for device in api_handler.get_devices():
        str_response += device.name + ", \n"
    return str_response


@app.route('/login')
def show_login_page():
    return send_from_directory('static/html/', "login_page.html")


# Flask WSGI API
@app.route('/do_login', methods=['GET', 'POST'])
def do_login():
    data = request.json
    from dynamic.login_handler import auth_user
    return "true" if auth_user(data["login"], data["password"]) else "false"


@app.route('/do_logout')
def do_logout():
    data = request.json


@app.route('/api', methods=['GET', 'POST'])
def send_to_api_handler():
    data = request.json
    return "true" if api_handler.handle(device = data["device"], action = data["action"]) else "false" # todo


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
    print("Initializing Devices")

    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)