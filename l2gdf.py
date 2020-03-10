names = open("cleanidmap.txt").read().splitlines()

print("Loaded names.")

from collections import Counter

indegree = Counter()

LOADINDEGREE = True
INDEGREEPATH = "indegree.pickle"

import pickle

if LOADINDEGREE:
	indegree = pickle.loads(open(INDEGREEPATH, "rb").read())
	print("Loaded indegree.")
else:

	with open("n2v.csv") as n2v:
		for line in n2v:
			line = line[:-1]
			line = line.split(" ", 1)
			indegree[line[1]] += 1

	with open(INDEGREEPATH, "wb+") as indegreefile:
		indegreefile.write(pickle.dumps(indegree))

	print("Wrote indegree.")

#exit(0)

#Need to do node size here because gephi doesn't get edges
header = "nodedef>name VARCHAR,label VARCHAR,X DOUBLE,Y DOUBLE,width DOUBLE\n"

i = open("largeout.csv")

i.readline()

with open("largeout.gdf", "w+") as f:
	f.write(header)
	for line in i:
		line = line.split()
		label = '"' + names[int(line[0])] + '"'
		f.write(f"{line[0]},{label},{line[1]},{line[2]},{indegree[line[0]]}\n")

f.close()
