from PIL import Image
import os
import sys

TILEPATH = "tiles"

imgpath = sys.argv[1]

Image.MAX_IMAGE_PIXELS = None
img = Image.open(imgpath)

print(img.size)

tw = 256
th = 256

os.mkdir("tiles")

for z in range(8, 0, -1):


    tx = img.size[0]//tw
    ty = img.size[1]//th

    print(tx, ty)

    for x in range(tx):
        for y in range(ty):
            print(x,y)
            bounds = (x*tw, y*th, (x+1)*tw, (y+1)*th)
            tile = img.crop(bounds)
            #tilefilename = f"{tw}-{th}-{x}-{y}-{'-'.join(str(b) for b in bounds)}.png"
            tilefilename = f"{z}-{x}-{y}.png"
            tile.save(os.path.join(TILEPATH, tilefilename))

    img = img.resize((img.size[0]//2, img.size[1]//2))
