import csv
from PIL import Image, ImageDraw, ImageFont
from time import time
from random import random, randint

data = []

w = h = 4096*4

img = Image.new("RGB", (w,h))
draw = ImageDraw.Draw(img)

"""
minx = None
miny = None
maxx = None
maxy = None
"""

minx = -52.368118
maxx = 56.263245
miny = -52.315582
maxy = 63.880695

with open("largeout.gdf", newline="") as csvfile:

	if None in [minx, miny, maxx, maxy]:
		reader = csv.reader(csvfile, delimiter=",", quotechar='"')

		next(reader, None)

		for ri, row in enumerate(reader):
		
			if ri%1000000 == 0:
				print(ri)
		
			x = float(row[2])
			y = float(row[3])
			
			if minx is None or x < minx:
				minx = x
			
			if maxx is None or x > maxx:
				maxx = x
			
			if miny is None or y < miny:
				miny = y
			
			if maxy is None or y > maxy:
				maxy = y
			
		csvfile.seek(0)
	
	reader = csv.reader(csvfile, delimiter=",", quotechar='"')

	next(reader, None)

	for ri, row in enumerate(reader):
	
		if ri%1000000 == 0:
			print(ri)
		
		try:
			x = float(row[2])
			y = float(row[3])
		except IndexError:
			print(row)
			exit(1)
		x = (x-minx)/(maxx-minx)*(w-1)
		y = (y-miny)/(maxy-miny)*(h-1)

		img.putpixel((int(x), int(y)), (128,128,128))

	csvfile.seek(0)
	
	font = ImageFont.truetype("NotoSansMono-Bold.ttf", 8)
	largefont = ImageFont.truetype("NotoSansMono-Bold.ttf", 50)
	
	fontcache = {
	
	}
	
	def large(n):
		n = int(n)
		if n not in fontcache:
			fontcache[n] = ImageFont.truetype("NotoSansMono-Bold.ttf", n)
		return fontcache[n]
	
	reader = csv.reader(csvfile, delimiter=",", quotechar='"')

	next(reader, None)

	for ri, row in enumerate(reader):
	
		if ri%1000000 == 0:
			print(ri)
			
		x = float(row[2])
		y = float(row[3])
		
		x = (x-minx)/(maxx-minx)*(w-1)
		y = (y-miny)/(maxy-miny)*(h-1)
		
		s = float(row[4])
		
		xy = (int(x), int(y))
		
		# if "Category:"
		if  s > 5000:
			#adjust size?
			draw.text(xy, text=row[1], font=large(10*(s/5000)**(1/2.71)), fill=(255,255,50,30))
		#if ri%1000 == 0:
		elif s/50000 > random():
			draw.text(xy, text=row[1], font=font)

print(minx, maxx, miny, maxy)

img.save(str(int(time()*1000)) + ".png")

#img.show()


