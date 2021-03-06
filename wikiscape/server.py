from io import BytesIO

from flask import Flask, request, send_from_directory, send_file, abort, jsonify
import flask_monitoringdashboard as dashboard
from settings import *

print("Creating app...")
app = Flask(__name__, static_url_path='')

"""
print("Loading dashboard...")
dashboard.config.init_from(file="dashboard.cfg")
print("Binding...")
dashboard.bind(app)
print("Done.")
"""

from quad import namequery, namesearch, termsuggest
from dynamic import generateTile, generateMeta

# keep this for local dev
@app.route('/tiles/<path:path>')
def send_tiles(path):

	# TODO nginx!
	try:
		return send_from_directory(TILECACHE, path)
	except:
		pass

	try:
		coords = path.split(".")[0]
		coords = [int(c) for c in coords.split("|")]
	except ValueError:
		abort(404)

	z, x, y = coords

	#z += 1
	#11
	if not ((1 < z < 17) and (0 < x < 2**(z-1)) and (0 < y < 2**(z-1))):#XXX z-1?
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

@app.route('/tilemeta/<path:path>')
def sent_tilemeta(path):

	try:
		coords = [int(c) for c in path.split("|")]
	except ValueError:
		abort(404)

	z, x, y = coords

	if not ((8 < z < 16) and (0 < x < 2**(z-1)) and (0 < y < 2**(z-1))):#XXX z-1?
		abort(404)

	return jsonify(generateMeta(z, x, y))


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

	print(x, y)

	return namequery(x, y)

@app.route("/search")
def search():
	title = request.args.get("search")
	coords = namesearch(title)

	print(coords)
	return jsonify(coords)

@app.route("/suggest")
def suggest():
	term = request.args.get("term")

	suggestions = termsuggest(term)

	# Only return page names, not size
	suggestions = [item[0] for item in suggestions]

	return jsonify(suggestions)#str([])#str(coords)

@app.route('/')
def root():
	return send_file('map.html')

if __name__ == "__main__":
	print("Starting server...")
	app.run()
