from math import log

from PIL import Image, ImageDraw, ImageFont

from quad import tree, keylist, valuelist, scalelist
from fonts import large

# Original image width and height (coordinate bounds)
ow = oh = 2**15
#Generate closer tiles dynamically?

def generateTile(zoom, x, y):

    # Tile width and height, dependent on zoom level
    zoomFactor = 2**(zoom-1)
    tw = ow/zoomFactor
    th = oh/zoomFactor

    # Tile radius
    tr = (tw**2 + th**2)**0.5

    tx = x*tw
    ty = y*th

    #print(tx, ty, tw, th, tr)
    points = tree.query_ball_point([(tx+tw/2, ty+th/2)], tr)[0]

    tile = Image.new("RGB", (256, 256))
    draw = ImageDraw.Draw(tile)

    for index in points:
        px, py = keylist[index]
        #print(px, py)
        if (tx <= px < tx+tw) and (ty <= py < ty+th):
            rx = (px-tx)*(zoomFactor/2**7)
            ry = (py-ty)*(zoomFactor/2**7)

            scale = scalelist[index]
            scale = 5*log(1+scale, 10)
            #scale = max(0, scale)
            #print("R", rx, ry)
            #print(px, py)
            point = (int(rx), int(ry))
            #tile.putpixel(point, (128,128,128))
            draw.ellipse([int(rx-scale), int(ry-scale), int(rx+scale), int(ry+scale)], fill=(200,200,200))

            if zoom >= 14:
                draw.text(point, valuelist[index], font=large(10))

    tilefilename = f"{zoom}-{x}-{y}.png"
    print("Generated", tilefilename, len(points))
    #tilepath = os.path.join(TILEPATH, tilefilename)
    #tile.save(tilepath)
    return tile
