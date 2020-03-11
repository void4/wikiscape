import csv

from scipy.spatial import KDTree, cKDTree

csvfile = open("largeout.gdf", newline="")

reader = csv.reader(csvfile, delimiter=",", quotechar='"')

next(reader, None)

data = {}

minx = -52.368118
maxx = 56.263245
miny = -52.315582
maxy = 63.880695

w = h = 2**15

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

	x = int(x)
	y = int(y)

	key = (x,y)
	data[key] = row[1]

tree = cKDTree(list(data.keys()))

keylist = list(data.keys())
valuelist = list(data.values())

def namequery(x,y):
	distances, indices = tree.query([[x,y]])
	return valuelist[indices[0]]
"""
print(tree.query([1000,1000]))
"""
