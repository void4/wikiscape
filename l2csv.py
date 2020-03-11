names = open("idmap.txt").read().splitlines()

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

i = open("largeout.csv")

i.readline()

with open("extended.csv", "w+") as f:
	for line in i:
		line = line.split()
		label = names[int(line[0])]
		f.write(f"{line[0]}\t{label}\t{line[1]}\t{line[2]}\t{indegree[line[0]]}\n")

f.close()
