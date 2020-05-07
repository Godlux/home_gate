from flask import Flask
from flask import request, send_from_directory
app = Flask(__name__)


@app.route('/')
def show_login_page():
    return send_from_directory('static/html/', "login_page.html")


@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static/ico/', "favicon.ico")


@app.route('/do_login', methods=['GET', 'POST'])
def do_login():
    data = request.json
    from dynamic.login_handler import auth_user
    return "true" if auth_user(data["login"], data["password"]) else "false"


@app.route('/do_logout')
def do_logout():
    data = request.json


@app.route('/api')
def activate():
    return 'Todo: handle api;'  # todo


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)