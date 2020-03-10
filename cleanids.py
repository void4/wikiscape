from string import ascii_uppercase, ascii_lowercase, digits

validchars = ascii_lowercase+ascii_uppercase+digits+" .():\n"

def clean(w):
	return "".join([c for c in w if c in validchars])#.replace("  ", " ")

nf = open("cleanidmap.txt", "w+")

for i, line in enumerate(open("idmap.txt")):
	if i % 1000000:
		print(i)
	nf.write(clean(line))


nf.close()
	
print("Wrote cleanidmap.txt")
