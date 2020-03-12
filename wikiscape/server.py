from io import BytesIO

from flask import Flask, request, send_from_directory, send_file, abort
import flask_monitoringdashboard as dashboard

print("Creating app...")
app = Flask(__name__, static_url_path='')

print("Loading dashboard...")
dashboard.config.init_from(file="dashboard.cfg")
print("Binding...")
dashboard.bind(app)
print("Done.")

from quad import namequery
from dynamic import generateTile

# keep this for local dev
@app.route('/tiles/<path:path>')
def send_tiles(path):
	#return send_from_directory('tiles', path)
	coords = path.split(".")[0]
	coords = [int(c) for c in coords.split("-")]

	z, x, y = coords

	if not ((10 < z < 15) and (0 < x < 2**(z-1)) and (0 < y < 2**(z-1))):#XXX z-1?
		abort(404)

	tile = generateTile(z, x, y)

	bio = BytesIO()
	tile.save(bio, "png")
	bio.seek(0)

	# Don't send image, send data instead

	#if z == 9:
	#	tile.save(f"/var/www/tiles/{z}-{x}-{y}.png")

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
	print("Starting server...")
	app.run()
