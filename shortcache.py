#tr -d '"\\' < combined.csv > clean.csv
# can omit ^ that ^ when running this
ID = 0
#use hex?

f = open("combined.csv")
o = open("short.csv", "w+")

cache = {}

def getId(w):
	global ID
	if w in cache:
		return cache[w]
	else:
		cache[w] = hex(ID)[2:]
		ID += 1
		return cache[w]

for li, line in enumerate(f):
	if li % 25000 == 0:
		print(li, ID)
	line = line[:-1]
	words = line.split(";")

	words = [getId(w) for w in words]
	
	line = ";".join(words) + "\n"
	o.write(line)
	
f.close()
o.close()

m = open("idmap.txt", "w+")
for key in cache:
	m.write(key + "\n")

m.close()
