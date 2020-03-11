import csv

from scipy.spatial import KDTree, cKDTree

CSVPATH = "extended.csv"
csvfile = open(CSVPATH, newline="")

reader = csv.reader(csvfile, delimiter="\t", quotechar='"')

next(reader, None)

data = {}

minx = -52.368118
maxx = 56.263245
miny = -52.315582
maxy = 63.880695

w = h = 2**15

keylist = []
valuelist = []

print(f"Loading {CSVPATH}...")

for ri, row in enumerate(reader):

	if ri%1000000 == 0:
		print(ri)

	try:
		x = float(row[2])
		y = float(row[3])
	except (IndexError, ValueError):
		print(row)
		exit(1)
	x = (x-minx)/(maxx-minx)*(w-1)
	y = (y-miny)/(maxy-miny)*(h-1)

	#x = int(x)
	#y = int(y)

	key = (x,y)
	keylist.append(key)
	valuelist.append(row[1])

print(f"Loaded {CSVPATH}.")

print("Constructing scipy.spatial.cKDTree...")
tree = cKDTree(keylist)
print("Quadtree constructed.")

def namequery(x,y):
	distances, indices = tree.query([[x,y]])
	return valuelist[indices[0]]
"""
print(tree.query([1000,1000]))
"""
