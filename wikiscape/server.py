from io import BytesIO

from flask import Flask, request, send_from_directory, send_file, abort

from quad import namequery
from dynamic import generateTile

app = Flask(__name__, static_url_path='')

# keep this for local dev
@app.route('/tiles/<path:path>')
def send_tiles(path):
	#return send_from_directory('tiles', path)
	coords = path.split(".")[0]
	coords = [int(c) for c in coords.split("-")]

	z, x, y = coords

	if not ((8 < z < 15) and (0 < x < 2**z) and (0 < y < 2**z)):
		abort(404)

	tile = generateTile(z, x, y)

	bio = BytesIO()
	tile.save(bio, "png")
	bio.seek(0)
	# Also cache in nginx data root?
	return send_file(bio, mimetype="image/png")

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
