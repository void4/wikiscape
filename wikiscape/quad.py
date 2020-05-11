import csv
import pickle

from scipy.spatial import KDTree, cKDTree

LOADTREE = False

LOADTRIE = True
SAVETRIE = False

CSVPATH = "extended.csv"
TREEPATH = "tree.pickle"
TRIEPATH = "trie.pickle"

if LOADTREE:
	print("Loading data...")
	keylist, valuelist, scalelist, tree = pickle.loads(open(TREEPATH, "rb").read())
else:
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
	scalelist = []

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
		scalelist.append(float(row[4]))

	print(f"Loaded {CSVPATH}.")

	print("Constructing scipy.spatial.cKDTree...")
	tree = cKDTree(keylist)
	print("Quadtree constructed.")

	"""
	with open(TREEPATH, "wb+") as treefile:
		treefile.write(pickle.dumps([keylist, valuelist, scalelist, tree]))

	print("Data saved.")
	"""

def namequery(x,y):
	distances, indices = tree.query([[x,y]])
	return valuelist[indices[0]]

import datrie
import string

if LOADTRIE:
	print("Loading search trie...")

	with open(TRIEPATH, "rb") as triefile:
		trie = pickle.loads(triefile.read())
	
	print("Trie loaded.")
else:
	print("Constructing search trie...")
	trie = datrie.Trie(string.ascii_lowercase)

	for vi, v in enumerate(valuelist):
		trie[v.lower()] = vi

	print("Trie constructed.")

	if SAVETRIE:
		print("Saving trie...")
		with open(TRIEPATH, "wb+") as triefile:
			triefile.write(pickle.dumps(trie))

		print("Trie saved.")

def termsuggest(term):

	# Search trie for term prefix
	suggestions = trie.items(term)

	# Sort suggestions by number of links, decreasing
	suggestions = sorted(suggestions, key=lambda item:scalelist[item[1]], reverse=True)


	return suggestions


def namesearch(title):
	suggestions = termsuggest(title)

	if len(suggestions) == 0:
		return {}

	closest = suggestions[0]

	x, y = keylist[closest[1]]
	
	z = 14
	
	#k = 2**(z-1)
	#return {"x":x/k, "y":y/k, "z":z}
	return {"x": x, "y":y, "z":z}

"""
print(tree.query([1000,1000]))
"""
