from PIL import ImageFont

font = ImageFont.truetype("NotoSansMono-Bold.ttf", 8)

fontcache = {

}

def large(n):
	n = int(n)
	if n not in fontcache:
		fontcache[n] = ImageFont.truetype("NotoSansMono-Bold.ttf", n)
	return fontcache[n]
