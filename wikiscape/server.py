from flask import Flask, request, send_from_directory, send_file

from quad import namequery

app = Flask(__name__, static_url_path='')

# keep this for local dev
@app.route('/tiles/<path:path>')
def send_tiles(path):
	return send_from_directory('tiles', path)

@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('css', path)

@app.route("/getmouse")
def getmouse():
	x = request.args.get("x")
	y = request.args.get("y")

	x = float(x)
	y = float(y)

	return namequery(x, y)

@app.route('/')
def root():
	return send_file('map.html')

if __name__ == "__main__":
	app.run()
