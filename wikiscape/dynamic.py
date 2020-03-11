from PIL import Image, ImageDraw, ImageFont

from quad import tree, keylist, valuelist
from fonts import large

# Original image width and height (coordinate bounds)
ow = oh = 2**15
#Generate closer tiles dynamically?

def generateTile(zoom, x, y):

    # Tile width and height, dependent on zoom level
    zoomFactor = 2**(zoom)
    tw = ow/zoomFactor
    th = oh/zoomFactor

    # Tile radius
    tr = (tw**2 + th**2)**0.5

    tx = x*tw
    ty = y*th

    #print(tx, ty, tw, th, tr)
    points = tree.query_ball_point([(tx+tw/2, ty+th/2)], tr)[0]

    tile = Image.new("RGB", (256, 256))

    for index in points:
        px, py = keylist[index]
        #print(px, py)
        if (tx <= px < tx+tw) and (ty <= py < ty+th):
            rx = (px-tx)*(zoomFactor/2**7)
            ry = (py-ty)*(zoomFactor/2**7)
            #print("R", rx, ry)
            #print(px, py)
            tile.putpixel((int(rx), int(ry)), (128,128,128))

    tilefilename = f"{zoom}-{x}-{y}.png"
    print("Generated", tilefilename, len(points))
    #tilepath = os.path.join(TILEPATH, tilefilename)
    #tile.save(tilepath)
    return tile
