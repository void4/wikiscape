import os
from math import log

from PIL import Image, ImageDraw, ImageFont

from quad import tree, keylist, valuelist, scalelist
from fonts import large
from settings import *

# Original image width and height (coordinate bounds)
ow = oh = 2**15
#Generate closer tiles dynamically?

#TILEPATH = "l12"
#os.makedirs(TILEPATH, exist_ok=True)

black = Image.new("RGB", (256, 256))


def tileCoords(zoom, x, y):
	# Tile width and height, dependent on zoom level
	zoomFactor = 2**(zoom-1)
	tw = ow/zoomFactor
	th = oh/zoomFactor

	# Tile radius
	tr = (tw**2 + th**2)**0.5

	tx = x*tw
	ty = y*th

	return zoomFactor,tw,th,tr,tx,ty

def generateMeta(zoom, x, y):
	#[{"text":"test", "value":[0,0]}]
	zoomFactor,tw,th,tr,tx,ty = tileCoords(zoom, x, y)

	points = tree.query_ball_point([(tx+tw/2, ty+th/2)], tr)[0]

	meta = []

	for index in points:
		scale = scalelist[index]
		if scale > 10:
			meta.append({"text":valuelist[index], "value":keylist[index], "scale":scale, "x":x, "y":y, "z":zoom})

	return meta

DRAWALL = True
DRAWLIMIT = 1000

def generateTile(zoom, x, y):


	zoomFactor,tw,th,tr,tx,ty = tileCoords(zoom, x, y)

	#print(tx, ty, tw, th, tr)
	points = tree.query_ball_point([(tx+tw/2, ty+th/2)], tr)[0]

	tilefilename = f"{zoom}|{x}|{y}.png"

	tilepath = os.path.join(TILECACHE, tilefilename)
	"""
	if len(points) == 0:
		black.save(tilepath)
		print("Generated", tilefilename, len(points))
		return None#XXX return black.png
	"""

	tile = Image.new("RGB", (256, 256))
	draw = ImageDraw.Draw(tile)

	draws = 0

	largest_scale = 0
	largest_index = None

	for index in points:
		px, py = keylist[index]
		#print(px, py)
		if (tx <= px < tx+tw) and (ty <= py < ty+th):
			rx = (px-tx)*(zoomFactor/2**7)
			ry = (py-ty)*(zoomFactor/2**7)

			scale = scalelist[index]

			if not DRAWALL and len(points) > DRAWLIMIT and scale < 100:
				continue

			if not DRAWALL and draws > DRAWLIMIT:
				break

			if scale > largest_scale:
				largest_scale = scale
				largest_index = index

			draws += 1

			scale = 5*log(1+scale, 10)
			#scale = max(0, scale)
			#print("R", rx, ry)
			#print(px, py)
			point = (int(rx), int(ry))

			if zoom >= 13:
				draw.ellipse([int(rx-scale), int(ry-scale), int(rx+scale), int(ry+scale)], fill=(100,100,000))
				draw.text(point, valuelist[index], font=large(10))
			else:
				if zoom >= 11:
					v = 200
				else:
					pix = tile.getpixel(point)
					v = min(255, pix[0]+32)
				tile.putpixel(point, (v,v,v))

	if largest_index and zoom < 13:
		draw.text((100, 128), valuelist[largest_index], font=large(12), fill=(200, 200, 50))

	print("Generated", tilefilename, len(points))
	#XXX save/cache tiles here anyway? not sure what is better, faster request or cached regions tile.save(tilepath)
	if zoom < 12:
		tile.save(tilepath)
	return tile

if __name__ == "__main__":
	for z in range(11, 12):
		for x in range(2**(z-1)):
			for y in range(2**(z-1)):
				generateTile(z, x, y)
